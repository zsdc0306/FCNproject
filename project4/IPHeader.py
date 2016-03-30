import socket
import random
from struct import *

class IPHeader:
    srcIP = ""
    dstIP = ""
    VER = 4
    IHL = 5
    typeOfService = 0
    totalLen = 0
    flag = 2  #don't fragment, 010
    fragOff = 0
    TTL = 255
    id = random.randint(1,60000)
    headerChecksum = 0
    protocol = socket.IPPROTO_TCP
    IPHeaderContent = ""

    def __init__(self,srcIP="",dstIP=""):
        self.srcIP = srcIP
        self.dstIP = dstIP
        self.VER = 4
        self.IHL = 5
        self.typeOfService = 0
        self.totalLen = 0
        self.flag = 2  #don't fragment, 010
        self.fragOff = 0
        self.TTL = 255
        self.id = random.randint(1,60000)
        self.headerChecksum = 0
        self.protocol = socket.IPPROTO_TCP

    def setIP(self,srcIP, dstIP):
        self.srcIP = srcIP
        self.dstIP = dstIP

    def getSrcIP(self):
        return self.srcIP

    def getDstIP(self):
        return self.dstIP

    def fillIPHeader(self):
        srcAddr = socket.inet_aton(self.srcIP)   #Spoof the source ip address if you want to
        dstAddr = socket.inet_aton (self.dstIP)
        VER_IHL = (self.VER << 4) + self.IHL
        flag_fragOff = (self.flag << 13) + self.fragOff
        # the ! in the pack format string means network order
        # B:8bit
        # H:16bit
        # 4s:32bit
        IPHeader = pack('!BBHHHBBH4s4s',VER_IHL, self.typeOfService, self.totalLen, self.id, flag_fragOff, self.TTL, self.protocol, self.headerChecksum, srcAddr, dstAddr)
        self.IPHeaderContent = IPHeader

    def unpackIPHeader(self, recvpack):
        ipHeader = unpack("!BBHHHBBH4s4s",recvpack[0][0:20])
        recvSrcIP = socket.inet_ntoa(ipHeader[8])
        recvDstIP = socket.inet_ntoa(ipHeader[9])
        self.setIP(recvSrcIP,recvDstIP)


