import socket
import packet
import random
import commands
import re
from HTTP import *
import urlparse
import packet
import time
from struct import *
from socket import *
import IPHeader
import TCPHeader



dstIP = "216.97.236.245"
srcIP = re.findall("inet addr:(.*)  Bcast", commands.getoutput('/sbin/ifconfig'))[0]
srcPort = random.randint(50000,60000)
dstPort = 80


class Ccnnection:
    """class of the packet, including TCPHeader, IPHeader"""
    def __init__(self,srcIP, dstIP, srcPort, dstPort):
        self.srcIP = srcIP
        self.dstIP = dstIP
        self.srcPort = srcPort
        self.dstPort = dstPort
        self.recvPacket = packet.Packet(srcIP,dstIP,srcPort,dstPort)
        self.sendPacket = packet.Packet(dstIP,srcIP,dstPort,srcPort)
        self.synPacket = packet.Packet(dstIP,srcIP,dstPort,srcPort)
        self.finPacket = packet.Packet(dstIP,srcIP,dstPort,srcPort)
        self.recvedPackCon = ""

    def startTransmit(self,sendsock,recvsock):
        self.setTCPConnection(sendsock,recvsock)
        self.sendPacket.sendPack(sendsock)
        self.recvPack(recvsock)
        while self.recvPacket.TCPHeader.fin != 1:
            self.sendPacket.sendPack(sendsock)
            self.recvPack(recvsock)
        return self.recvedPackCon


    def recvPack(self,sock):
        recvbuff= sock.recvfrom(65535)
        # win = self.c_window
        startTime = time.time()
        while 1:
            if time.time() - startTime > 60000: #set timeout
                self.c_window = 1               #reset congestion window
                break
            ipHeader = unpack("!BBHHHBBH4s4s",recvbuff[0][0:20])
            tcpHeader = unpack("!HHLLHHHH",recvbuff[0][20:40])
            recvSrcIP = inet_ntoa(ipHeader[8])
            recvDstIP = inet_ntoa(ipHeader[9])
            recvSrcPort = tcpHeader[0]
            recvDstPort = tcpHeader[1]
            if recvSrcIP == self.dstIP and recvDstIP == self.srcIP and recvSrcPort == self.dstPort and recvDstPort == self.srcPort:
                recvPack = packet.Packet(recvSrcIP,recvDstIP,recvSrcPort,recvDstPort)
                recvPack.unPackPacket(recvbuff)
                if recvPack.TCPHeader.syn == 1 or recvPack.TCPHeader.fin ==1:
                    self.recvPacket = recvPack
                    return
                if recvPack.TCPHeader.seqNum != self.sendPacket.TCPHeader.ackNum or recvPack.TCPHeader.ackNum != (self.sendPacket.TCPHeader.seqNum+len(self.sendPacket.TCPHeader.data)):
                    return
                else:
                    self.recvPacket = recvPack
                    self.recvedPackCon += recvPack.TCPHeader.data
                    print "segment data:^^^^^^^^^^^^^^^^^^^^^^^^^^^^" + recvPack.TCPHeader.data
                    return
            else:
                recvbuff = sock.recvfrom(65535)

        # TODO if not checkChecksum(recvbuff):
        # tcpHeader = recvpack[0][20:44]
        # tcp_hdr = unpack("!HHLLBBHHHL",tcpHeader)
        # srcPort = tcp_hdr[0]
        # dstPort = tcp_hdr[1]
        # seqNum = tcp_hdr[2]
        # ackNum = tcp_hdr[3]
        # print ackNum
        # window = tcp_hdr[5]



    def setTCPConnection(self,sendsocket,recvsocket):
        synSeq = 0
        self.synPacket.TCPHeader.setSeq(synSeq)
        self.synPacket.TCPHeader.setAck(0)
        self.synPacket.setPktTpye(SYN)
        self.synPacket.packPacket("")
        # connectionPack.rawSend(sendsocket,connectionPack.pktcontent,(dstIP,0))
        self.synPacket.sendPack(sendsocket)
        self.recvPack(recvsocket)
        seqNum = self.recvPacket.TCPHeader.seqNum
        ackNum = self.recvPacket.TCPHeader.ackNum
        self.sendPacket.TCPHeader.setSeq(ackNum)
        self.sendPacket.TCPHeader.setAck(seqNum+1)
        self.sendPacket.setPktTpye(ACK)
        self.sendPacket.sendPack(sendsocket)
        # connectionPack.rawSend(sendsocket,connectionPack.pktcontent,(dstIP,0))
        # print connectionPack.pktcontent
        # print connectionPack.TCPHeader.ackNum
        print "connection set"
        return





















SYN = 1
ACK = 2
PSH = 3
FIN = 4

TargetData = ""

user_data = ""

#
# def setTCPConnection(sendsocket, recvsocket):
#     synpack = packet.Packet(srcIP,dstIP,srcPort,dstPort)
#     #send SYN pack
#     synSeq = random.randint(0,100000)
#     synpack.TCPHeader.setSeq(synSeq)
#     synpack.TCPHeader.setAck(0)
#     synpack.packPacket(SYN,"")
#     pktContent = synpack.getPktCon()
#     synpack.rawSend(sendsocket,pktContent,(dstIP,0))
#     synAckPack = packet.Packet(dstIP,srcIP,dstPort,srcPort)
#     synAckPack = synAckPack.recvPack(recvsocket)
#     #to check whether the port and ip of receive packet is the oppisite we send
#     seqNum = synAckPack.TCPHeader.getSeq()
#     ackNum = synAckPack.TCPHeader.getAck()
#     ackPack = packet.Packet(srcIP,dstIP,srcPort,dstPort)
#     ackPack.TCPHeader.setAck(seqNum+1)
#     ackPack.TCPHeader.setSeq(ackNum)
#     ackPack.packPacket(ACK,"")
#     pktContent = ackPack.getPktCon()
#     ackPack.rawSend(sendsocket,pktContent,(dstIP,0))
#     return ackPack



    #******************************************************************
    # pack = packet.Packet(srcIP,dstIP,srcPort,dstPort)
    # #send SYN pack
    # pack.TCPHeader.setSeq(0)
    # pack.TCPHeader.setAck(0)
    # synPack = pack.packPacket(SYN,"")
    # pack.sendPack(sendsocket,synPack,(dstIP,0))
    # synAckPack = packet.Packet(dstIP,srcIP,dstPort,srcPort)
    # synAckPack = synAckPack.recvPack(recvsocket)
    # #to check whether the port and ip of receive packet is the oppisite we send
    # seqNum = synAckPack.TCPHeader.getSeq()
    # ackNum = synAckPack.TCPHeader.getAck()
    # pack.TCPHeader.setAck(seqNum+1)
    # pack.TCPHeader.setSeq(ackNum)
    # ackPack = pack.packPacket(ACK,"")
    # pack.sendPack(sendsocket,ackPack,(dstIP,0))
    # return pack



