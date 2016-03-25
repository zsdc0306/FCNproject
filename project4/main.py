import socket
import packet
import random

dstIP = "216.97.236.245"
srcIP = "10.103.9.68"
srcPort = random.randint(50000,60000)
dstPort = 80

SYN = 1
ACK = 2
PSH = 3
FIN = 4



user_data = ""

import socket
import urlparse


CRLF = "\r\n"
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




def setTCPConnection(sendsocket, recvsocket):
    pack = packet.Packet()
    #send SYN pack
    pack.TCPHeader.setSeq(0)
    pack.TCPHeader.setAck(0)
    synPack = pack.packPacket(SYN,"",srcIP,dstIP,srcPort,dstPort)
    pack.sendPack(sendsocket,synPack,(dstIP,0))
    synAckPack = packet.RecvPack().recvPack(recvsocket,dstIP,srcIP,dstPort,srcPort)
    #to check whether the port and ip of receive packet is the oppisite we send
    seqNum = synAckPack.TCPHeader.getSeq()
    ackNum = synAckPack.TCPHeader.getAck()
    pack.TCPHeader.setAck(seqNum+1)
    pack.TCPHeader.setSeq(ackNum)
    ackPack = pack.packPacket(ACK,"",srcIP,dstIP,srcPort,dstPort)
    pack.sendPack(sendsocket,ackPack,(dstIP,0))


sendsock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
recvsock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)

setTCPConnection(sendsock,recvsock)

user_data = get("http://david.choffnes.com/")
pack = packet.Packet()
pack.TCPHeader.setSeq(0)
pack.TCPHeader.setAck(0)
getpack = pack.packPacket(PSH,user_data,srcIP,dstIP,srcPort,dstPort)
pack.sendPack(sendsock,getpack,(dstIP,0))








