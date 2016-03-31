import random
import socket
import IPHeader
import TCPHeader
from struct import *
from socket import *
import binascii
import time

SYN = 1
ACK = 2
PSH = 3
FIN = 4
MSS = 536


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
        self.c_window = 1
        self.pktcontent=""
        self.pktTYPE = 0


    def getPktCon(self):
        return self.pktcontent

    def setSegmentBuffer(self,TCPHeader,IPHeader):
        self.segmentTCPBuffer = TCPHeader
        self.segmentIPBuffer = IPHeader
        self.segmentIPBuffer = 1

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
        print "syn=" + str(syn)
        self.TCPHeader.setFlag(syn,ack,fin,psh,rst,urg)
        self.pktTYPE = pktType

    def packPacket(self, userData):
        IPheader = self.IPHeader
        IPheader.fillIPHeader()
        IPheaderContent = IPheader.IPHeaderContent
        TCPheader = self.TCPHeader
        TCPheader.fillPseTCPHeader(self.srcIP, self.dstIP, userData)
        TCPheaderContent = TCPheader.TCPHeaderContent
        self.pktcontent = IPheaderContent + TCPheaderContent +userData

    def rawSend(self, socket, content, addr):
        socket.sendto(content, addr)

    def sendPack(self,sock):
        self.packPacket(self.TCPHeader.data)
        sock.sendto(self.pktcontent,(self.dstIP,0))

    def unPackPacket(self,pack):
        self.pktcontent = pack[0]
        self.IPHeader.unpackIPHeader(pack)
        self.TCPHeader.unpackTCPHeader(pack)





