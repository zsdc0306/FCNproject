import socket
import packet
import random
import commands
import re
from HTTP import *
import urlparse



dstIP = "216.97.236.245"
srcIP = re.findall("inet addr:(.*)  Bcast", commands.getoutput('/sbin/ifconfig'))[0]
srcPort = random.randint(50000,60000)
dstPort = 80


SYN = 1
ACK = 2
PSH = 3
FIN = 4

TargetData = ""

user_data = ""

#
# def setTCPConnection(sendsocket, recvsocket):
#     synpack = packet.Packet(srcIP,dstIP,srcPort,dstPort)
#     #send SYN pack
#     synSeq = random.randint(0,100000)
#     synpack.TCPHeader.setSeq(synSeq)
#     synpack.TCPHeader.setAck(0)
#     synpack.packPacket(SYN,"")
#     pktContent = synpack.getPktCon()
#     synpack.rawSend(sendsocket,pktContent,(dstIP,0))
#     synAckPack = packet.Packet(dstIP,srcIP,dstPort,srcPort)
#     synAckPack = synAckPack.recvPack(recvsocket)
#     #to check whether the port and ip of receive packet is the oppisite we send
#     seqNum = synAckPack.TCPHeader.getSeq()
#     ackNum = synAckPack.TCPHeader.getAck()
#     ackPack = packet.Packet(srcIP,dstIP,srcPort,dstPort)
#     ackPack.TCPHeader.setAck(seqNum+1)
#     ackPack.TCPHeader.setSeq(ackNum)
#     ackPack.packPacket(ACK,"")
#     pktContent = ackPack.getPktCon()
#     ackPack.rawSend(sendsocket,pktContent,(dstIP,0))
#     return ackPack


def setTCPConnection(sendsocket,recvsocket):
    connectionPack = packet.Packet(srcIP,dstIP,srcPort,dstPort)
    synSeq = 0
    connectionPack.TCPHeader.setSeq(synSeq)
    connectionPack.TCPHeader.setAck(0)
    connectionPack.packPacket(SYN, "")
    # connectionPack.rawSend(sendsocket,connectionPack.pktcontent,(dstIP,0))
    sendsocket.sendto(connectionPack.pktcontent,(dstIP,0))
    connectionPack.recvPack(recvsocket)
    seqNum = connectionPack.TCPHeader.seqNum
    ackNum = connectionPack.TCPHeader.ackNum
    connectionPack.TCPHeader.setSeq(ackNum)
    connectionPack.TCPHeader.setAck(seqNum+1)
    connectionPack.packPacket(ACK, "")
    # connectionPack.rawSend(sendsocket,connectionPack.pktcontent,(dstIP,0))
    sendsocket.sendto(connectionPack.pktcontent,(dstIP,0))
    # print connectionPack.pktcontent
    # print connectionPack.TCPHeader.ackNum
    print "connection set"
    return connectionPack


    #******************************************************************
    # pack = packet.Packet(srcIP,dstIP,srcPort,dstPort)
    # #send SYN pack
    # pack.TCPHeader.setSeq(0)
    # pack.TCPHeader.setAck(0)
    # synPack = pack.packPacket(SYN,"")
    # pack.sendPack(sendsocket,synPack,(dstIP,0))
    # synAckPack = packet.Packet(dstIP,srcIP,dstPort,srcPort)
    # synAckPack = synAckPack.recvPack(recvsocket)
    # #to check whether the port and ip of receive packet is the oppisite we send
    # seqNum = synAckPack.TCPHeader.getSeq()
    # ackNum = synAckPack.TCPHeader.getAck()
    # pack.TCPHeader.setAck(seqNum+1)
    # pack.TCPHeader.setSeq(ackNum)
    # ackPack = pack.packPacket(ACK,"")
    # pack.sendPack(sendsocket,ackPack,(dstIP,0))
    # return pack



def recvAck(sendsocket, recvsocket):
    recvPacket = packet.Packet(dstIP,srcIP,dstPort,srcPort)
    recvPacket = recvPacket.recvPack(recvsocket)
    #to check whether the port and ip of receive packet is the oppisite we send
    seqNum = recvPacket.TCPHeader.getSeq()
    ackNum = recvPacket.TCPHeader.getAck()
    ackPack = packet.Packet(srcIP,dstIP,srcPort,dstPort)
    ackPack.TCPHeader.setAck(seqNum+len(recvPacket.segmentData))
    # print "segment len" + str(len(recvPacket.segmentData))
    ackPack.TCPHeader.setSeq(ackNum)
    ackPack.packPacket(ACK,"")
    # print "send seq:" + str(ackPack.TCPHeader.seqNum)
    # print "send ack:"+ str(ackPack.TCPHeader.ackNum)
    ackPack.sendPack(sendsocket,ackPack.getPktCon(),(dstIP,0))
    return recvPacket.segmentData

