import string
import urlparse
import sys
import os
import socket
from struct import *
import binascii
import struct
import random
# if len(sys.argv)<2:
# 	print "You need input target url"
# 	sys.exit(0)
#
# url = urlparse.urlparse(sys.argv[1])
# dstHost = url.netloc
# dstIP = socket.gethostbyname(dstHost)
# path = url.path
# if url.path == '' or path[-1] == '/':
# 	filename = 'index.html'
# else:
# 	filename = path.split('/')[-1]
dstIP = "216.97.236.245"
#srcIP = socket.gethostbyname(socket.gethostname())
srcIP = "10.103.9.68"
CRLF = "\r\n"

srcPort = random.randint(50000,60000)




def get(url):
	url = urlparse.urlparse(url)
	host = url.netloc
	path = url.path
	if url.path == '':
		path = '/'
	HTTP_Protocol = 'GET '+path+' HTTP/1.1'
	Request_Header = [
		HTTP_Protocol,
		"Host: "+host,
		"Connection: keep-alive",
		"Cache-Control: max-age=0",
		"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
		"Upgrade-Insecure-Requests: 1",
		"DNT: 1",
		"Accept-Language: en-US,en;q=0.8,zh-CN;q=0.6",
		"",
		"",
	]
	Request = CRLF.join(Request_Header)
	return Request























#IP packet

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



# ip header fields
def fillIPHeader(srcip, dstip, ihl=5,ver=4,tos=0,ip_tot_len =0, flag = 0, fragoff = 0, ttl = 255, ip_check =0):
	ip_ver = ver
	ip_ihl = ihl
	ip_tos = tos
	ip_tot_len = ip_tot_len  # kernel will fill the correct total length
	ip_id = 29525   #Id of this packet
	ip_flag = flag   #set flag as not fragment, 010,
	ip_frag_off = fragoff
	ip_ttl = ttl
	ip_proto = socket.IPPROTO_TCP
	ip_check = 0    # kernel will fill the correct checksum
	ip_saddr = socket.inet_aton (srcip)   #Spoof the source ip address if you want to
	ip_daddr = socket.inet_aton (dstip)
	ip_ihl_ver = (ip_ver << 4) + ip_ihl
	#ip_flag_frag_off = 0
	ip_flag_frag_off = (ip_flag << 13) + ip_frag_off
	# the ! in the pack format string means network order
	# B:8bit
	# H:16bit
	# 4s:32bit
	ip_header = pack('!BBHHHBBH4s4s', ip_ihl_ver, ip_tos, ip_tot_len, ip_id, ip_flag_frag_off, ip_ttl, ip_proto, ip_check, ip_saddr, ip_daddr)
	return ip_header



# 0                   1                   2                   3   
#     0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 
#    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#    |          Source Port          |       Destination Port        |
#    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#    |                        Sequence Number                        |
#    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#    |                    Acknowledgment Number                      |
#    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#    |  Data |           |U|A|P|R|S|F|                               |
#    | Offset| Reserved  |R|C|S|S|Y|I|            Window             |
#    |       |           |G|K|H|T|N|N|                               |
#    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#    |           Checksum            |         Urgent Pointer        |
#    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#    |                    Options                    |    Padding    |
#    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#    |                             data                              |
#    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+



# tcp header fields

def fillTCPHeader(srcport, dstport ,seq_num, ack_num, tcp_offset_res, tcp_flags, window, checksum, urgpointer):
	tcp_header = pack('!HHLLBBHHH' , srcport, dstport ,seq_num, ack_num, tcp_offset_res, tcp_flags,window, checksum, urgpointer)
	return tcp_header

def fillPseTCPHeader(srcport, dstport ,seq_num, ack_num, user_data, windows, ack=0, syn=0, rst=0, psh=0,fin=0, urg =0, checksum = 0, urgpointer =0, doff =5):
	tcp_source = srcport   # source port
	tcp_dest = dstport   # destination port
	tcp_seq = seq_num
	tcp_ack_seq = ack_num
	tcp_doff = doff    # 4 bit field, size of tcp header, 5 * 4 = 20 bytes
	# tcp flags
	tcp_window = windows    # maximum allowed window size
	tcp_check = checksum
	tcp_urg_ptr = urgpointer
	tcp_offset_res = (tcp_doff << 4) + 0 # the ! in the pack format string means network order
	tcp_flags = fin + (syn << 1) + (rst << 2) + (psh <<3) + (ack << 4) + (urg << 5)
	TCPHeader = fillTCPHeader(tcp_source, tcp_dest ,tcp_seq, tcp_ack_seq, tcp_offset_res,tcp_flags, tcp_window, tcp_check, tcp_urg_ptr)
	placeholder = 0
	source_address = socket.inet_aton(srcIP)
	dest_address = socket.inet_aton(dstIP)
	protocol = socket.IPPROTO_TCP
	tcp_length = len(TCPHeader) + len(user_data)
	psh = pack('!4s4sBBH' , source_address , dest_address , placeholder , protocol , tcp_length);
	psh = psh + TCPHeader + user_data;
	tcp_check = calchecksum(psh)
    #print tcp_checksum
    # make the tcp header again and fill the correct checksum - remember checksum is NOT in network byte order
	tcp_header = pack('!HHLLBBH' , srcport, dstport, seq_num, ack_num, tcp_offset_res, tcp_flags,  windows) + pack('H', tcp_check) + pack('!H' , urgpointer)
	return tcp_header


# checksum functions needed for calculation checksum
def calchecksum( msg):
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

#create file
#tar_file = open(filename,'w')

sendsock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
recvsock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
recvsock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP)

user_data = ""


IPHeader = fillIPHeader(srcIP,dstIP)
TCPHeader = fillPseTCPHeader(srcPort,80, 0, 0, user_data, socket.htons (5840),0, 1)
# final full packet - syn packets dont have any data
packet = IPHeader + TCPHeader + user_data
#Send the packet finally - the port specified has no effect
sendsock.sendto(packet, (dstIP , 0 ))    # put this in a loop if you want to flood the target


pkt= recvsock.recvfrom(65535)
print len(pkt[0])



print pkt

ethernetHeader=pkt[0][0:14]

eth_hdr = unpack("6s6s2s",ethernetHeader)

binascii.hexlify(eth_hdr[0])

binascii.hexlify(eth_hdr[1])

binascii.hexlify(eth_hdr[2])

ipHeader = pkt[0][0:20]

ip_hdr = unpack("!4s4s4s4s4s",ipHeader)

print "Source IP address:"+socket.inet_ntoa(ip_hdr[3])

print "Destination IP address:"+socket.inet_ntoa(ip_hdr[4])

tcpHeader = pkt[0][20:44]

tcp_hdr = struct.unpack("!HHLLBBHHHL",tcpHeader)


seqNum = tcp_hdr[2]
ackNum = tcp_hdr[3]
print ackNum
window = tcp_hdr[5]



IPHeader = fillIPHeader(srcIP,dstIP)
TCPHeader = fillPseTCPHeader(srcPort,80,ackNum,seqNum+1,"",socket.htons(window),1)
packet = IPHeader + TCPHeader + user_data
#Send the packet finally - the port specified has no effect
sendsock.sendto(packet, (dstIP, 0 ))    # put this in a loop if you want to flood the target

user_data = get("http://david.choffnes.com/")
TCPHeader = fillPseTCPHeader(srcPort,80,ackNum,seqNum+1,user_data,socket.htons(window),1,0,0,1)

packet = IPHeader + TCPHeader + user_data
sendsock.sendto(packet, (dstIP , 0 ))


#recvsock.recvfrom(4096)
# recvsock.connect((dstIP,80))
# recvsock.recv(4096)
