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
        # self.c_window = 2
        self.pktcontent=""
        self.segmentData = ""
        self.nextExpectedSeq = -1
        self.segmentTCPBuffer = TCPHeader.TCPHeader()
        self.segmentIPBuffer = IPHeader.IPHeader()
        self.isSegmentBuffer = 0


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

    def sendPack(self,socket,content,addr):
        socket.sendto(content, addr)




    def recvPack(self,sock):
        recvbuff= sock.recvfrom(65535)
        # win = self.c_window
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

                # if recvTCPheader.syn == 1 or recvTCPheader.fin == 1:
                #      break
                # if recvTCPheader.psh == 1:
                #     self.segmentData += recvTCPheader.data
                #     self.setNextSeq(recvTCPheader.seqNum + len(recvTCPheader.data))
                #     #self.c_window += 1
                #     break
                # else:
                self.segmentData += recvTCPheader.data
                self.setNextSeq(recvTCPheader.seqNum + len(recvTCPheader.data))


                # if self.nextExpectedSeq != -1:
                #     print "recvbuffer\r\n" + recvTCPheader.data
                #     print "nextSeq\r\n" + str(self.nextExpectedSeq) + "seq :" +str(recvTCPheader.seqNum)
                #     if recvTCPheader.seqNum != self.nextExpectedSeq:
                #         self.setSegmentBuffer(recvTCPheader,recvIPheader)
                #         recvbuff = sock.recvfrom(65535)
                #         win -= 1
                #         if win==0:
                #             print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
                #             print self.segmentData
                #             break
                #         else:
                #             continue
                #     else:
                #         self.setNextSeq(recvTCPheader.seqNum + len(recvTCPheader.data))
                #         self.segmentData += recvTCPheader.data
                #         if self.isSegmentBuffer == 1:
                #             if self.nextExpectedSeq == self.segmentTCPBuffer.seqNum:
                #                 self.segmentData += self.segmentTCPBuffer.data
                #                 self.TCPHeader = self.segmentTCPBuffer
                #                 self.IPHeader = self.segmentIPBuffer
                #                 print "#################################################"
                #                 print self.segmentData
                #                 break
                #             else:
                #                 self.TCPHeader = recvTCPheader
                #                 self.IPHeader = recvIPheader
                #                 print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                #                 print self.segmentData
                #                 break
                #         elif win ==0:
                #             print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
                #             print self.segmentData
                #             break
                #         else:
                #             recvbuff = sock.recvfrom(65535)
                #             continue
                # else:
                #     self.segmentData += recvTCPheader.data
                #     self.setNextSeq(recvTCPheader.seqNum + len(recvTCPheader.data))
                #     recvbuff = sock.recvfrom(65535)
                #     win -= 1
                #     if win == 0:
                #         print "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
                #         print self.segmentData
                #         break
                #     else:
                #         continue

                # print "^^^^^^^^^^^^^^^^^^^^^psh" + str(recvTCPheader.psh)
                # print "syn:" + str(recvTCPheader.syn) + "ack:" + str(recvTCPheader.ack) + "fin:" + str(recvTCPheader.fin)
                # packlen = packlen - 1
                # print packlen
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











