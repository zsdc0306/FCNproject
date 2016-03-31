import socket
import packet
import random
import commands
import re
import HTTP
import connection



SYN = 1
ACK = 2
PSH = 3
FIN = 4

# def createPacket(seq,ack,TYPE,userData):
#     pack = packet.Packet(srcIP,dstIP,srcPort,dstPort)
#     pack.TCPHeader.setAck(ack)
#     pack.TCPHeader.setSeq(seq)
#     pack.packPacket(TYPE,userData)
#     return pack





Request = HTTP.HTTPRequest("http://david.choffnes.com/")
Request.sendGetRequest()



#
#
# pack = packet.Packet(srcIP,dstIP,srcPort,dstPort)
# user_data_get = HTTP.get("http://david.choffnes.com/")
# pack.sendTCPHeader.data = user_data_get
# pack.startTransmit(sendsock,recvsock)
# print pack.segmentData
# getpack = createPacket(conAckPack.TCPHeader.getSeq(),conAckPack.TCPHeader.getAck(),PSH,user_data_get)

# pkt = getpack.startTransmit(sendsock,recvsock)
# print pkt



# getAckPack = createPacket(getpack.TCPHeader.getAck(),getpack.TCPHeader.getSeq()+len(user_data_get),ACK,"")
# data =""
# buffer = HTTP.RecvData(sendsock,recvsock)
# while buffer:
#     data = HTTP.RecvData(sendsock,recvsock)
#     data += data
# print data

