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
        self.TCPHeader = TCPHeader.TCPHeader()
        self.IPHeader = IPHeader.IPHeader()
        self.srcIP = srcIP
        self.dstIP = dstIP
        self.srcPort = srcPort
        self.dstPort = dstPort
        self.TCPHeader.setPort(self.srcPort,self.dstPort)
        self.IPHeader.setIP(self.srcIP, self.dstIP)
        self.c_window = 1
        self.pktcontent=""
        self.segmentData = ""
        self.nextExpectedSeq = -1
        self.segmentTCPBuffer = TCPHeader.TCPHeader()
        self.segmentIPBuffer = IPHeader.IPHeader()
        self.isSegmentBuffer = 0
        self.pktTYPE = 2


    def getPktCon(self):
        return self.pktcontent

    def setSegmentBuffer(self,TCPHeader,IPHeader):
        self.segmentTCPBuffer = TCPHeader
        self.segmentIPBuffer = IPHeader
        self.segmentIPBuffer = 1


    def getSegData(self):
        return self.segmentData

    def setNextSeq(self,seq):
        self.nextExpectedSeq = seq

    def packPacket(self,PKT_TYPE, userData):
        ack = 0
        syn = 0
        rst = 0
        psh = 0
        fin = 0
        urg = 0
        if PKT_TYPE == SYN:
            syn = 1
        elif PKT_TYPE == ACK:
            ack = 1
        elif PKT_TYPE == PSH:
            psh = 1
            ack = 1
        elif PKT_TYPE == FIN:
            fin = 1
        IPheader = self.IPHeader
        IPheader.fillIPHeader()
        IPheaderContent = IPheader.IPHeaderContent
        TCPheader = self.TCPHeader
        TCPheader.setFlag(syn,ack,fin,psh,rst,urg)
        TCPheader.fillPseTCPHeader(self.srcIP, self.dstIP, userData)
        TCPheaderContent = TCPheader.TCPHeaderContent
        self.pktcontent = IPheaderContent + TCPheaderContent +userData

    def rawSend(self, socket, content, addr):
        socket.sendto(content, addr)

    def sendPack(self,sock):
        self.TCPHeader.setAck(self.TCPHeader.seqNum)
        self.TCPHeader.setSeq(self.TCPHeader.ackNum)
        self.packPacket(self.pktTYPE,"")
        sock.sendto(self.pktcontent,(self.dstIP,0))


    def startTransmit(self,sendsock,recvsock):
        self.sendPack(sendsock)
        self.recvPack(recvsock)
        while self.TCPHeader.fin != 1:
            self.sendPack(sendsock)
            self.recvPack(recvsock)
        return self.segmentData


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
                recvIPheader = IPHeader.IPHeader()
                recvTCPheader = TCPHeader.TCPHeader()
                recvIPheader.unpackIPHeader(recvbuff)
                recvTCPheader.unpackTCPHeader(recvbuff)
                if recvTCPheader.syn == 1 or recvTCPheader.fin ==1:
                    self.TCPHeader = recvTCPheader
                    print self.TCPHeader.seqNum
                    self.IPHeader = recvIPheader
                    return
                if recvTCPheader.seqNum != self.TCPHeader.ackNum or recvTCPheader.ackNum != (self.TCPHeader.seqNum+len(self.TCPHeader.data)):
                    return
                else:
                    self.TCPHeader = recvTCPheader
                    self.IPHeader = recvIPheader
                    self.segmentData += recvTCPheader.data
                    print "segment data:^^^^^^^^^^^^^^^^^^^^^^^^^^^^" + recvTCPheader.data
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
        self.TCPHeader.setSeq(synSeq)
        self.TCPHeader.setAck(0)
        self.packPacket(SYN, "")
        # connectionPack.rawSend(sendsocket,connectionPack.pktcontent,(dstIP,0))
        sendsocket.sendto(self.pktcontent,(self.dstIP,0))
        self.recvPack(recvsocket)
        seqNum = self.TCPHeader.seqNum
        ackNum = self.TCPHeader.ackNum
        self.TCPHeader.setSeq(ackNum)
        self.TCPHeader.setAck(seqNum+1)
        self.packPacket(ACK, "")
        # connectionPack.rawSend(sendsocket,connectionPack.pktcontent,(dstIP,0))
        sendsocket.sendto(self.pktcontent,(self.srcIP,0))
        # print connectionPack.pktcontent
        # print connectionPack.TCPHeader.ackNum
        print "connection set"
        return self








