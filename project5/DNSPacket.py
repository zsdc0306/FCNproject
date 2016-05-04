from struct import pack,unpack
import random

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


class DNSHeader():
    def __init__(self):
        self.id = random.randint(1, 65535)
        self.flags = 0
        self.qdcount = 0
        self.ancount = 0
        self.nscount = 0
        self.arcount = 0
        self.header_content=""

    # unpack the DNS header and set the parameter to the attribute
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
                      self.arcount
                      )
        self.header_content = header
        return 1

    def setHeader(self, id, flags, qdcount, ancount, nscount, arcount):
        self.id = id
        self.flags = flags
        self.qdcount = qdcount
        self.ancount = ancount
        self.nscount = nscount
        self.arcount = arcount
        return 1


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
        answer = pack('!HHHIH',
                      self.name,
                      self.type,
                      self.a_class,
                      self.ttl,
                      self.length
                      )
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


class DNSQuery():
    def __init__(self):
        self.qname_len = 0
        self.qname = ""
        self.qtype = ""
        self.qclass = ""
        self.query_content = ""

    def get_qname(self, query):
        length = 0
        qname = ""
        for byte in query:
            if unpack('!B',byte) == "0":
                length += 1
                break
            else:
                index = unpack('!B', byte)
                length += 1
                while index:
                    print length
                    qname += unpack('!c', query[length])
                    index -= 1
                    length += 1
        self.qname_len = length
        self.qname = query[0:length]
