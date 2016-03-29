import socket
import random
from struct import *

class TCPHeader:
    def __init__(self, srcPort=0, dstPort = 80):
        self.srcPort = srcPort #set the source port as a random port between 50000 and 60000
        self.dstPort = dstPort
        self.seqNum = 0
        self.ackNum = 0
        self.window = 4096
        self.ack = 0
        self.syn = 0
        self.rst = 0
        self.psh = 0
        self.fin = 0
        self.urg = 0
        self.urgPointer = 0
        self.checkSum = 0
        self.dataOffSet = 5
        self.option = 0
        self.data = ""

    def setFlag(self, syn, ack, fin, psh, rst, urg):
        self.syn = syn
        self.ack = ack
        self.psh = psh
        self.rst = rst
        self.urg = urg
        self.fin = fin

    def setPort(self,srcPort,dstPort):
        self.srcPort = srcPort
        self.dstPort = dstPort

    def setSeq(self,seqNum):
        self.seqNum = seqNum

    def setAck(self,ackNum):
        self.ackNum = ackNum

    def getSeq(self):
        return self.seqNum

    def getAck(self):
        return self.ackNum

    def setWindow(self,window):
        self.window = window

    def getWindow(self):
        return self.window

    def getCheckSum(self):
        return self.checkSum

    def setChecksum(self,checksum):
        self.checkSum = checksum

    def fillPseTCPHeader(self,srcIP, dstIP, userData):
        OffSetRes = (self.dataOffSet << 4) + 0 # the ! in the pack format string means network order
        flags = self.fin + (self.syn << 1) + (self.rst << 2) + (self.psh <<3) + (self.ack << 4) + (self.urg << 5)
        TCPHeader = pack('!HHLLBBHHH',self.srcPort, self.dstPort ,self.seqNum, self.ackNum, OffSetRes,flags, self.window, self.checkSum, self.urgPointer)
        placeholder = 0
        source_address = socket.inet_aton(srcIP)
        dest_address = socket.inet_aton(dstIP)
        protocol = socket.IPPROTO_TCP
        tcp_length = len(TCPHeader) + len(userData)
        pseheader = pack("!4s4sBBH", source_address, dest_address, placeholder, protocol, tcp_length)
        header = pseheader + TCPHeader + userData
        pseHeader_check = self.calchecksum(header)
        # make the tcp header again and fill the correct checksum - remember checksum is NOT in network byte order
        tcp_header = pack('!HHLLBBH' , self.srcPort, self.dstPort, self.seqNum, self.ackNum, OffSetRes, flags,  self.window) + pack('H', pseHeader_check) + pack('!H' , self.urgPointer)
        return tcp_header

    # checksum functions needed for calculation checksum
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

    def unpackTCPHeader(self,recvpack):
        tcpHeader = recvpack[0][20:40]
        tcp_hdr = unpack("!HHLLBBHHH",tcpHeader)
        srcPort = tcp_hdr[0]
        dstPort = tcp_hdr[1]
        seqNum = tcp_hdr[2]
        ackNum = tcp_hdr[3]
        offset_res = tcp_hdr[4]
        flags = tcp_hdr[5]
        offset = offset_res >> 4
        flagtmp = flags
        urg = flags >> 5
        flagtmp -= (urg << 5)
        ack = flagtmp >> 4
        flagtmp -= (ack <<4)
        psh = flagtmp >> 3
        flagtmp -= (psh << 3)
        rst = flagtmp >> 2
        flagtmp -= (rst << 2)
        syn = flagtmp >> 1
        flagtmp -= syn << 1
        fin = flagtmp
        window = tcp_hdr[6]
        checksum = tcp_hdr[7]
        self.setSeq(seqNum)
        self.setAck(ackNum)
        self.setWindow(window)
        self.setPort(srcPort,dstPort)
        self.setFlag(syn,ack,fin,psh,rst,urg)
        self.setChecksum(checksum)
        if offset == 6:
            self.option = recvpack[0][40:44]
            self.data = recvpack[0][44:]
        self.data = recvpack[0][40:]