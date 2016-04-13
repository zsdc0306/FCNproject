import sys
from struct import pack, unpack
import socket
import SocketServer
import random
import urllib
import urllib2

# ref: http://www.binarytides.com/dns-query-code-in-c-with-winsock/
# DNS packets
# +---------------------+
# | Header              |
# +---------------------+
# | Question            | the question for the name server
# +---------------------+
# | Answer              | RRs answering the question
# +---------------------+
# | Authority           | RRs pointing toward an authority
# +---------------------+
# | Additional          | RRs holding additional information
# +---------------------+

# DNS Header
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
# |                     ID                        |
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
# |QR| Opcode    |AA|TC|RD|RA| Z      |  RCODE    |
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
# |                   QDCOUNT                     |
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
# |                   ANCOUNT                     |
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
# |                   NSCOUNT                     |
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
# |                   ARCOUNT                     |
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

# query
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
# |                                               |
# /                    QNAME                      /
# /                                               /
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
# |                    QTYPE                      |
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
# |                    QCLASS                     |
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+

# Answer
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
# /                       NAME                    /
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
# |                       TYPE                    |
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
# |                      CLASS                    |
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
# |                       TTL                     |
# |                                               |
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
# |                     RDLENGTH                  |
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--|
# /                      RDATA                    /
# +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+


class fastestIP():
    def __init__(self):
        self.ip="54.85.32.37"

    def getIP(self):
        return self.ip


class DNSHeader():
    def __init__(self):
        self.id = random.randint(1, 65535)
        self.flags = 0
        self.qdcount = 0
        self.ancount = 0
        self.nscount = 0
        self.arcount = 0
        self.header_content=""

    def unpack(self, data):
        self.header_content = data
        content = data
        header = unpack('!HHHHHH',content)
        self.id = header[0]
        self.flags = header[1]
        self.qdcount = header[2]
        self.ancount = header[3]
        self.nscount = header[4]
        self.arcount = header[5]
        return 1

    def pack(self):
        header = pack('!HHHHHH',
                      self.id,
                      self.flags,
                      self.qdcount,
                      self.ancount,
                      self.nscount,
                      self.arcount)
        self.header_content = header
        return 1

    def setHeader(self,id,flags,qdcount, ancount,nscount,arcount):
        self.id = id
        self.flags = flags
        self.qdcount = qdcount
        self.ancount = ancount
        self.nscount = nscount
        self.arcount = arcount
        return 1



class DNSAnswer():
    def __init__(self):
        self.name = 0
        self.type = 0
        self.a_class = 0
        self.ttl =0
        self.answer_content = ""
        self.length = 0
        self.data = ""

    def pack(self):
        answer = pack('!HHHIH',self.name,self.type,self.a_class,self.ttl,self.length)
        answer += self.data
        self.answer_content = answer
        return 1

    def setAnswer(self,name,type,aclass,ttl,length,data):
        self.name = name
        self.type = type
        self.a_class = aclass
        self.ttl = ttl
        self.length = length
        self.data = data


class DNSHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        print len(data)
        print "\n"
        mysocket = self.request[1]
        recvDNSheader = DNSHeader()
        recvDNSheader.unpack(data[:12])
        sendDNSheader = DNSHeader()
        sendDNSheader.setHeader(recvDNSheader.id,0b1000000110000000,1,1,0,0)
        sendDNSheader.pack()
        Question = data[12:17]
        DNSanswer = DNSAnswer()
        ip = fastestIP().getIP()
        ip = socket.inet_aton(ip)
        DNSanswer.setAnswer(0xc00c,1,1,600,4,ip)
        DNSanswer.pack()
        print len(Question)
        print "^^^^^^^^"
        print len(DNSanswer.answer_content)
        sendmsg = sendDNSheader.header_content + Question + DNSanswer.answer_content
        mysocket.sendto(sendmsg,self.client_address)



try:
    name = sys.argv[4]
    port = int(sys.argv[2])
except Exception:
    print 'You need input port and name. Exiting Program.'
    sys.exit()

server = SocketServer.UDPServer(('',port),DNSHandler)
server.serve_forever()
