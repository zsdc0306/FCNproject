import random
import socket
import IPHeader
import TCPHeader
from struct import *
from socket import *
import binascii

SYN = 1
ACK = 2
PSH = 3
FIN = 4


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
        self.segmentData =""

    def getPktCon(self):
        return self.pktcontent

    def getSegData(self):
        return self.segmentData



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
        IPHeaderContent = IPheader.fillIPHeader()
        TCPheader = self.TCPHeader
        TCPheader.setFlag(syn,ack,fin,psh,rst,urg)
        TCPHeaderContent = TCPheader.fillPseTCPHeader(self.srcIP, self.dstIP, userData)
        self.pktcontent = IPHeaderContent + TCPHeaderContent +userData

    def sendPack(self,socket,content,addr):
        socket.sendto(content, addr)

    def recvPack(self,sock):
        recvbuff= sock.recvfrom(65535)
        packlen = 2
        while 1:
            ipHeader = unpack("!BBHHHBBH4s4s",recvbuff[0][0:20])
            tcpHeader = unpack("!HHLLHHHH",recvbuff[0][20:40])
            recvSrcIP = inet_ntoa(ipHeader[8])
            recvDstIP = inet_ntoa(ipHeader[9])
            recvSrcPort = tcpHeader[0]
            recvDstPort = tcpHeader[1]
            if recvSrcIP == self.srcIP and recvDstIP == self.dstIP and recvSrcPort == self.srcPort and recvDstPort == self.dstPort:
                recvIPheader = self.IPHeader
                recvTCPheader = self.TCPHeader
                recvIPheader.unpackIPHeader(recvbuff)
                recvTCPheader.unpackTCPHeader(recvbuff)
                if recvTCPheader.syn == 1 or recvTCPheader.fin == 1:
                    break
                else:
                    self.segmentData += recvTCPheader.data
                    packlen = packlen - 1
                    print packlen
                    if packlen == 0:
                        break
                    else:
                        recvbuff=sock.recvfrom(65535)
            else:
                recvbuff = sock.recvfrom(65535)
        print len(recvbuff[0])
        # TODO if not checkChecksum(recvbuff):

        return self
        # tcpHeader = recvpack[0][20:44]
        # tcp_hdr = unpack("!HHLLBBHHHL",tcpHeader)
        # srcPort = tcp_hdr[0]
        # dstPort = tcp_hdr[1]
        # seqNum = tcp_hdr[2]
        # ackNum = tcp_hdr[3]
        # print ackNum
        # window = tcp_hdr[5]











