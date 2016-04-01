import socket
import random
from struct import *


class IPHeader:
    def __init__(self, srcIP="", dstIP=""):
        self.srcIP = srcIP
        self.dstIP = dstIP
        self.VER = 4
        self.IHL = 5
        self.typeOfService = 0
        self.totalLen = 0
        self.flag = 2  # don't fragment, 010
        self.fragOff = 0
        self.TTL = 255
        self.id = random.randint(1, 60000)
        self.headerChecksum = 0
        self.protocol = socket.IPPROTO_TCP
        self.IPHeaderContent = ""

    def setIP(self, srcIP, dstIP):
        self.srcIP = srcIP
        self.dstIP = dstIP

    def getSrcIP(self):
        return self.srcIP

    def getDstIP(self):
        return self.dstIP

    # IP packet

    # 0                   1                   2                   3
    #     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    #    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    #    |Version|  IHL  |Type of Service|          Total Length         |
    #    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    #    |         Identification        |Flags|      Fragment Offset    |
    #    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    #    |  Time to Live |    Protocol   |         Header Checksum       |
    #    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    #    |                       Source Address                          |
    #    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    #    |                    Destination Address                        |
    #    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    #    |                    Options                    |    Padding    |
    #    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+




    # make the ip header
    def fillIPHeader(self):
        srcAddr = socket.inet_aton(self.srcIP)  # Spoof the source ip address if you want to
        dstAddr = socket.inet_aton(self.dstIP)
        VER_IHL = (self.VER << 4) + self.IHL
        flag_fragOff = (self.flag << 13) + self.fragOff
        # the ! in the pack format string means network order
        # B:8bit
        # H:16bit
        # 4s:32bit
        IPHeader = pack('!BBHHHBBH4s4s', VER_IHL, self.typeOfService, self.totalLen, self.id, flag_fragOff, self.TTL,
                        self.protocol, self.headerChecksum, srcAddr, dstAddr)
        self.IPHeaderContent = IPHeader

    def unpackIPHeader(self, recvpack):
        ipHeader = unpack("!BBHHHBBH4s4s", recvpack[0][0:20])
        self.IPHeaderContent = ipHeader
        recvSrcIP = socket.inet_ntoa(ipHeader[8])
        recvDstIP = socket.inet_ntoa(ipHeader[9])
        self.setIP(recvSrcIP, recvDstIP)
