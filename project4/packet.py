import random
import socket
import IPHeader
import TCPHeader
from struct import *
from socket import *
import binascii
import time


#flag of packet type
SYN = 1
ACK = 2
PSH = 3
FIN = 4

class Packet:
    """class of the packet, including TCPHeader, IPHeader"""
    def __init__(self,srcIP, dstIP, srcPort, dstPort):
        self.srcIP = srcIP
        self.dstIP = dstIP
        self.srcPort = srcPort
        self.dstPort = dstPort
        self.TCPHeader = TCPHeader.TCPHeader()
        self.IPHeader = IPHeader.IPHeader()
        self.TCPHeader.setPort(self.srcPort,self.dstPort)
        self.IPHeader.setIP(self.srcIP, self.dstIP)
        self.c_window = 1                                            # congesting window, initial set as 1
        self.pktcontent=""                                           # the string format of the packet, used to send to the server
        self.pktTYPE = 0                                             # pktTYPE, as SYN,FIN,ACK,PSH
        self.userData = ""                                           #user data, it is the same as TC{Header.data


    def getPktCon(self):
        return self.pktcontent


    def setNextSeq(self,seq):
        self.nextExpectedSeq = seq

    def setPktTpye(self,pktType):
        syn,ack,fin,psh,rst,urg = 0,0,0,0,0,0
        if pktType == SYN:
            syn = 1
        elif pktType == ACK:
            ack = 1
        elif pktType == PSH:
            psh = 1
            ack = 1
        elif pktType == FIN:
            fin = 1
            ack = 1
        self.TCPHeader.setFlag(syn,ack,fin,psh,rst,urg)
        self.pktTYPE = pktType



    # pack the packet with the parameter of its own and set the packetcontent
    def packPacket(self):
        IPheader = self.IPHeader
        IPheader.fillIPHeader()
        IPheaderContent = IPheader.IPHeaderContent
        TCPheader = self.TCPHeader
        TCPheader.fillPseTCPHeader(self.srcIP, self.dstIP, self.userData)
        TCPheaderContent = TCPheader.TCPHeaderContent
        self.TCPHeader.data = self.userData
        self.pktcontent = IPheaderContent + TCPheaderContent +self.userData


    def rawSend(self, socket, content, addr):
        socket.sendto(content, addr)

    # pack the packet and then send it to the server
    def sendPack(self,sock):
        self.packPacket()
        sock.sendto(self.pktcontent,(self.dstIP,0))

    # unpack the packet and fill the information of TCPHeader and IPHeader.
    def unPackPacket(self,pack):
        self.pktcontent = pack[0]
        self.IPHeader.unpackIPHeader(pack)
        self.TCPHeader.unpackTCPHeader(pack)


    def calchecksum(self,msg):
        s = 0
        if len(msg) % 2 != 0:
            msg += pack('B', 0)
        for i in range(0, len(msg), 2):
            w = ord(msg[i]) + (ord(msg[i+1]) << 8)
            s = s + w

        s = (s >> 16) + (s & 0xffff)
        s = s + (s >> 16)
        s = ~s & 0xffff

        return s


