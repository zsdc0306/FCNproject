import socket
import packet
import random
import commands
import re
import HTTP
import connection



dstIP = connection.dstIP
srcIP = connection.srcIP
dstPort = 80
srcPort = connection.srcPort

SYN = 1
ACK = 2
PSH = 3
FIN = 4

def createPacket(seq,ack,TYPE,userData):
    pack = packet.Packet(srcIP,dstIP,srcPort,dstPort)
    pack.TCPHeader.setAck(ack)
    pack.TCPHeader.setSeq(seq)
    pack.packPacket(TYPE,userData)
    return pack

sendsock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
recvsock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)


conAckPack = connection.setTCPConnection(sendsock,recvsock)
print "connection set"
user_data_get = HTTP.get("http://david.choffnes.com/")
getpack = createPacket(conAckPack.TCPHeader.getSeq(),conAckPack.TCPHeader.getAck(),PSH,user_data_get)
getpack.sendPack(sendsock,getpack.getPktCon(),(dstIP,0))

RequestPack = createPacket(getpack..TCPHeader.getSeq(),conAckPack.TCPHeader.getAck(),ACK,"")

# getAckPack = createPacket(getpack.TCPHeader.getAck(),getpack.TCPHeader.getSeq()+len(user_data_get),ACK,"")
data =""
buffer = HTTP.RecvData(sendsock,recvsock)
while buffer:
    data = HTTP.RecvData(sendsock,recvsock)
    data += data
print data

