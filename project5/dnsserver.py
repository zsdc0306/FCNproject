import sys
import socket
import SocketServer
import DNSPacket
import getopt
import TestRTT
import collections
import cache
import time

# ec2-54-88-98-7.compute-1.amazonaws.com	Origin server (running Web server on port 8080)
# ec2-54-85-32-37.compute-1.amazonaws.com		N. Virginia
# ec2-54-193-70-31.us-west-1.compute.amazonaws.com	N. California
# ec2-52-38-67-246.us-west-2.compute.amazonaws.com	Oregon
# ec2-52-51-20-200.eu-west-1.compute.amazonaws.com	Ireland
# ec2-52-29-65-165.eu-central-1.compute.amazonaws.com	Frankfurt
# ec2-52-196-70-227.ap-northeast-1.compute.amazonaws.com	Tokyo
# ec2-54-169-117-213.ap-southeast-1.compute.amazonaws.com	Singapore
# ec2-52-63-206-143.ap-southeast-2.compute.amazonaws.com	Sydney
# ec2-54-233-185-94.sa-east-1.compute.amazonaws.com	Sao Paulo

cache_TTL = 10 * 60  # defalut set 10 min as cache timeout
thread_timeout = 0.8  # defalut set 0.8s as thread timeout

replica_host = [
    'ec2-54-85-32-37.compute-1.amazonaws.com',
    'ec2-54-193-70-31.us-west-1.compute.amazonaws.com',
    'ec2-52-38-67-246.us-west-2.compute.amazonaws.com',
    'ec2-52-51-20-200.eu-west-1.compute.amazonaws.com',
    'ec2-52-29-65-165.eu-central-1.compute.amazonaws.com',
    'ec2-52-196-70-227.ap-northeast-1.compute.amazonaws.com',
    'ec2-54-169-117-213.ap-southeast-1.compute.amazonaws.com',
    'ec2-52-63-206-143.ap-southeast-2.compute.amazonaws.com',
    'ec2-54-233-185-94.sa-east-1.compute.amazonaws.com',
]

replica_host_dic = {
    'ec2-54-85-32-37.compute-1.amazonaws.com': "54.85.32.37",
    'ec2-54-193-70-31.us-west-1.compute.amazonaws.com': "54.193.70.31",
    'ec2-52-38-67-246.us-west-2.compute.amazonaws.com': "52.38.67.246",
    'ec2-52-51-20-200.eu-west-1.compute.amazonaws.com': "52.51.20.200",
    'ec2-52-29-65-165.eu-central-1.compute.amazonaws.com': "52.29.65.165",
    'ec2-52-196-70-227.ap-northeast-1.compute.amazonaws.com': "52.196.70.227",
    'ec2-54-169-117-213.ap-southeast-1.compute.amazonaws.com': "54.169.117.213",
    'ec2-52-63-206-143.ap-southeast-2.compute.amazonaws.com': "52.63.206.143",
    'ec2-54-233-185-94.sa-east-1.compute.amazonaws.com': "54.233.185.94",
}


ip_table_geo = {
    "Virginia": "54.193.70.31",
    "California": "54.193.70.31",
    "Oregon": "52.38.67.246",
    "Ireland": "52.51.20.200",
    "Frankfurt": "52.29.65.165",
    "Tokyo": "52.196.70.227",
    "Singapore": "54.169.117.213",
    "Sydney": "52.63.206.143",
    "SaoPaulo": "54.233.185.94"
}

#
# query_c""
# name = name.split(".")
# for part in name:
#     query_content += pack("!B", len(part))
#     for byte in bytes(part):
#         query_content += pack("!c", byte)
# query_content += pack('!B',0)
# QNAMELen = len(query_content)


class FastestIP():
    def __init__(self):
        self.ip = "54.85.32.37"
        self.cache = cache.cache("dnscache.json")
        self.start_time = time.time()

    def getIP(self, client_addr):
        end_time = time.time()
        if end_time - self.start_time > cache_TTL:
            self.cache.clear_cache()    # set time to clear the cache
            self.start_time = time.time()
        if self.cache.get(client_addr) != -1:
            self.ip = self.cache.get(client_addr)
            return self.ip
        else:
            threadlist = []
            for host in replica_host:
                t = TestRTT.TestRTTThread(host, port, client_addr)
                t.start()
                threadlist.append(t)
            for t in threadlist:
                t.join(thread_timeout)  # set 1s as timeout
            bestreplica = self.sortdic(TestRTT.replica_host_delay)
            self.ip = replica_host_dic[bestreplica]
            if TestRTT.replica_host_delay[bestreplica] < 100:
                self.cache.set(client_addr, self.ip)
            return self.ip

    def sortdic(self, latency_dic):
        sorteddic = collections.OrderedDict(sorted(latency_dic.items(), key=lambda t: t[1]))
        print sorteddic
        best_replica = sorteddic.keys()[0]  # get the best replica host
        # print "host:" + best_replica + "latency:" + str(sorteddic[best_replica])
        return best_replica


class DNSHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request[0]
        mysocket = self.request[1]
        recvDNSheader = DNSPacket.DNSHeader()
        recvDNSheader.unpack(data[:12])
        sendDNSheader = DNSPacket.DNSHeader()
        sendDNSheader.setHeader(recvDNSheader.id, 0b1000000110000000, 1, 1, 0, 0)
        sendDNSheader.pack()
        question = data[12:17]
        dnsanswer = DNSPacket.DNSAnswer()
        ip = FastestIP().getIP(self.client_address[0])
        ip = socket.inet_aton(ip)
        dnsanswer.setAnswer(0xc00c, 1, 1, 600, 4, ip)
        dnsanswer.pack()
        sendmsg = sendDNSheader.header_content + question + dnsanswer.answer_content
        mysocket.sendto(sendmsg, self.client_address)

opts, args = getopt.getopt(sys.argv[1:], "p:n:")

port = 0
try:
    for op, value in opts:
        if op == "-p":
            port = int(value)
        if op == "-n":
            name = value
except Exception as e:
    print "ERROR:" + e.message
    sys.exit(0)

# ip = fastestIP()
# print "$$$$" + ip.getIP("129.10.117.100")
#


server = SocketServer.UDPServer(('', port), DNSHandler)
try:
    server.serve_forever()
except KeyboardInterrupt:
    server.server_close()
    cache.cache().clear_cache()

