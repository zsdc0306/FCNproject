import socket
import packet
import random
import commands
import re
from HTTP import *
import packet
import time
from struct import *
from socket import *
import socket


SYN = 1
ACK = 2
PSH = 3
FIN = 4

class Ccnnection:
    """class of the connection, with all function related to connection, for example three way handshake"""
    def __init__(self, dstIP, dstPort):
        self.srcIP = re.findall("inet addr:(.*)  Bcast", commands.getoutput('/sbin/ifconfig'))[0]      # get the source ip address with system command
        self.dstIP = dstIP
        self.srcPort = random.randint(50000,60000)                                                     # set the source port as a random one
        self.dstPort = dstPort
        self.sendPacket = packet.Packet(self.srcIP,dstIP,self.srcPort,dstPort)                        # create 4 packet object for different use, send packet is used to record the last send packet
        self.recvPacket = packet.Packet(dstIP,self.srcIP,dstPort,self.srcPort)
        self.synPacket = packet.Packet(self.srcIP,dstIP,self.srcPort,dstPort)
        self.finPacket = packet.Packet(self.srcIP,dstIP,self.srcPort,dstPort)
        self.sendsocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
        self.recvsocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        self.recvedPackCon = ""                                                                       # record the received data
        self.c_window = 1

    def setRequestPack(self,userData):                                                                # used to set the HTTP request packet, as the PSH packet
        self.sendPacket.setPktTpye(PSH)
        self.sendPacket.userData = userData
        self.sendPacket.packPacket()

    def setAckPack(self):                                                                             # set the ack packet
        self.sendPacket.setPktTpye(ACK)                                                               # type is ack
        self.sendPacket.TCPHeader.setSeq(self.recvPacket.TCPHeader.ackNum)                            # the sequence number is receive packet's sequence number
        if self.recvPacket.TCPHeader.fin == 1 or self.recvPacket.TCPHeader.syn == 1:                  # if the revepacket is syn packet of fin packet, the acknowledge numb plus 1,
            self.sendPacket.TCPHeader.setAck(self.recvPacket.TCPHeader.seqNum + 1)
        else:
            self.sendPacket.TCPHeader.setAck(self.recvPacket.TCPHeader.seqNum + len(self.recvPacket.TCPHeader.data))   # otherwise is plus length of data
        self.sendPacket.userData = ""                                                                 # ack packet dose not has data
        self.sendPacket.packPacket()

    def startTransmit(self):
        self.sendPacket.sendPack(self.sendsocket)
        self.recvPack()
        while self.recvPacket.TCPHeader.fin != 1:
            self.sendPacket.sendPack(self.sendsocket)
            self.recvPack()
        self.setAckPack()                                                                           # get the fin packet, ack the fin packet and tear the connection
        self.sendPacket.sendPack(self.sendsocket)
        self.setTearDown()
        print "connection done"
        return



    def recvPack(self):
        recvbuff= self.recvsocket.recvfrom(65535)
        # win = self.c_window
        startTime = time.time()
        while 1:
            if time.time() - startTime > 60000:                                                                                         #set timeout
                self.c_window = 1                                                                                                        #reset congestion window
                break
            ipHeader = unpack("!BBHHHBBH4s4s",recvbuff[0][0:20])                                                                            # unpack the receive buffer to check the ip and port
            tcpHeader = unpack("!HHLLHHHH",recvbuff[0][20:40])
            recvSrcIP = inet_ntoa(ipHeader[8])
            recvDstIP = inet_ntoa(ipHeader[9])
            recvSrcPort = tcpHeader[0]
            recvDstPort = tcpHeader[1]
            if recvSrcIP == self.dstIP and recvDstIP == self.srcIP and recvSrcPort == self.dstPort and recvDstPort == self.srcPort:              # to check whether the received packet is from the target server
                recvPack = packet.Packet(self.dstIP,self.srcIP,self.dstPort,self.srcPort)
                recvPack.unPackPacket(recvbuff)
                if recvPack.TCPHeader.syn == 1 or recvPack.TCPHeader.fin ==1:
                    self.recvPacket = recvPack
                    self.sendPacket.TCPHeader.setSeq(self.recvPacket.TCPHeader.ackNum)
                    self.sendPacket.TCPHeader.setAck(self.recvPacket.TCPHeader.seqNum+1)
                    self.sendPacket.setPktTpye(ACK)
                    window = min(self.sendPacket.TCPHeader.window, self.recvPacket.TCPHeader.window)                                               #merge the window
                    self.sendPacket.TCPHeader.window = window
                    return
                if recvPack.TCPHeader.ack == 1 and recvPack.TCPHeader.data == "":
                    recvbuff = self.recvsocket.recvfrom(65535)
                    self.recvPacket = recvPack
                    continue
                if recvPack.TCPHeader.seqNum != self.sendPacket.TCPHeader.ackNum or recvPack.TCPHeader.ackNum != (self.sendPacket.TCPHeader.seqNum+len(self.sendPacket.TCPHeader.data)):
                                                                        # to match whether the sequence number is expected one, if not, return the receive method, the sendpacket is not updated so it will resend the former ack packet
                    return
                else:
                    self.recvPacket = recvPack                                                             # match the legal packet and store it to the recvpacket
                    self.recvedPackCon += recvPack.TCPHeader.data
                    self.setAckPack()
                    window = min(self.sendPacket.TCPHeader.window, self.recvPacket.TCPHeader.window)                                               #merge the window
                    self.sendPacket.TCPHeader.window = window
                    self.c_window += 1                                                                     # once receive packet successfully, increase congestion window
                    if self.c_window>1000:
                        self.c_window = self.c_window / 2                                                  # fix the congestion window
                    return
            else:
                recvbuff = self.recvsocket.recvfrom(65535)

        # TODO if not checkChecksum(recvbuff):
        # tcpHeader = recvpack[0][20:44]
        # tcp_hdr = unpack("!HHLLBBHHHL",tcpHeader)
        # srcPort = tcp_hdr[0]
        # dstPort = tcp_hdr[1]
        # seqNum = tcp_hdr[2]
        # ackNum = tcp_hdr[3]
        # print ackNum
        # window = tcp_hdr[5]



    def setTCPConnection(self):                                                         # three way handshake
        synSeq = random.randint(10000,300000)                                           # initial the sequence number as a random number
        self.synPacket.TCPHeader.setSeq(synSeq)
        self.synPacket.TCPHeader.setAck(0)
        self.synPacket.setPktTpye(SYN)
        # connectionPack.rawSend(sendsocket,connectionPack.pktcontent,(dstIP,0))
        self.synPacket.sendPack(self.sendsocket)
        self.recvPack()
        self.sendPacket.sendPack(self.sendsocket)
        # connectionPack.rawSend(sendsocket,connectionPack.pktcontent,(dstIP,0))
        # print connectionPack.pktcontent
        # print connectionPack.TCPHeader.ackNum
        print "connection set"
        return



    def setTearDown(self):
        self.finPacket.setPktTpye(FIN)                                                  # dend the Fin packet
        self.finPacket.TCPHeader.setSeq(self.recvPacket.TCPHeader.ackNum)
        self.finPacket.TCPHeader.setAck(self.recvPacket.TCPHeader.seqNum + 1)
        self.finPacket.packPacket()
        self.finPacket.sendPack(self.sendsocket)


