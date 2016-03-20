import string
import urlparse
import sys
import os
import socket
from struct import *

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
srcIP = "192.168.1.15"

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
def fillIPHeader(srcip, dstip, ihl=5,ver=4,tos=0,ip_tot_len =0, flag = 2, fragoff = 0, ttl = 255, ip_check =0):
	ip_ver = ver
	ip_ihl = ihl
	ip_tos = tos
	ip_tot_len = ip_tot_len  # kernel will fill the correct total length
	ip_id = 54321   #Id of this packet
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



class Packet(object):
	"""class of the packet, including TCPHeader, IPHeader"""
	def __init__(self, arg):
		super(Packet, self).__init__()
		self.arg = arg
		





# tcp header fields

def fillTCPHeader(srcport, dstport ,seq_num, ack_num, windows, tcp_flags, checksum = 0, urgpointer =0, doff =5):
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
	tcp_header = pack('!HHLLBBHHH' , tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags,tcp_window, tcp_check, tcp_urg_ptr)
	return tcp_header

def fillPseTCPHeader(srcport, dstport ,seq_num, ack_num, user_data, windows, ack=0, syn=0, rst=0, psh=0,fin=0, urg =0, checksum = 0, urgpointer =0, doff =5):
    tcp_flags = fin + (syn << 1) + (rst << 2) + (psh <<3) + (ack << 4) + (urg << 5)
    TCPHeader = fillTCPHeader(srcport, dstport ,seq_num, ack_num, windows,tcp_flags, checksum, urgpointer, doff)
    placeholder = 0
    protocol = socket.IPPROTO_TCP
    tcp_length = len(TCPHeader) + len(user_data)
    psh = pack('!4s4sBBH' , srcIP , dstIP , placeholder , protocol , tcp_length);
    psh = psh + TCPHeader + user_data;
    tcp_check = calchecksum(psh)
    #print tcp_checksum
    # make the tcp header again and fill the correct checksum - remember checksum is NOT in network byte order
    tcp_header = pack('!HHLLBBH' , srcport, dstport, seq_num, ack_num, ((doff << 4) + 0), tcp_flags,  windows) + pack('H' , tcp_check) + pack('!H' , urgpointer)
    return tcp_header

# checksum functions needed for calculation checksum
def calchecksum(msg):
    s = 0

    # loop taking 2 characters at a time
    for i in range(0, len(msg), 2):
        w = ord(msg[i]) + (ord(msg[i+1]) << 8 )
        s = s + w
    s = (s>>16) + (s & 0xffff);
    s = s + (s >> 16);

    #complement and mask to 4 byte short
    s = ~s & 0xffff
    return s



#create file
#tar_file = open(filename,'w')

sendsock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
recvsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP)

user_data = ""


IPHeader = fillIPHeader(srcIP,dstIP)
TCPHeader = fillPseTCPHeader(42525, 80, 24242, 0, user_data, 65535, 0, 1)
# final full packet - syn packets dont have any data
packet = IPHeader + TCPHeader + user_data
#Send the packet finally - the port specified has no effect
sendsock.sendto(packet, (dstIP , 0 ))    # put this in a loop if you want to flood the target

recvsock.connect((dstIP,80))
recvsock.recv(4096)