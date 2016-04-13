import os

# 0 1        2 3 4   5    6       7 8   9   10 11
# r 1.332528 2 3 tcp 1040 ------- 1 0.0 3.0 31 225
# + 1.332592 3 2 ack 50 ------- 1 0.0 3.0 31 225
# - 1.332592 2 3 tcp 1040 ------- 1 0.0 3.0 31 225
# tokens[0]: +, -, r
# tokens[1]: time
# tokens[2]: src node
# tokens[3]: dest node
# tokens[4]: packet type/proto
# tokens[5]: packet size

def calThroughput(TCPType, CBRRate):
	startTime1 = 0
	startTime2 = 0
	endTime1 = 0
	endTime2 = 0
	filename = TCPType + "_" + str(CBRRate) + ".tr"
	filecon = open(filename)
	line = filecon.readline()
	while line:
		tokens = line.split(' ')
		if tokens[7] == "1":
			if tokens[2] == "0" and tokens[0] == "+":
				startTime1 = float(tokens[1])
			if tokens[0] == "r":
				packetRecv1 += tokens[5] * 8
				endTime1 = float(tokens[1])
		elif tokens[7] == "2":
			if tokens[2] == "4" and tokens[0] == "+":
				startTime2 = float(tokens[1])
			if tokens[0] == "r":
				packetRecv2 += tokens[5] * 8
				endTime2 = float(tokens[1])

	throughput1 = packetRecv1/(endTime1 - startTime1) / (1024*1024)
	throughput2 = packetRecv2/(endTime2 - startTime2) / (1024*1024)
	return str(throughput1) + '\t' + str(throughput2)


def calDropRate(TCPType, CBRrate):
	filename = TCPType + "_" + str(CBRRate) + ".tr"
	filecon = open(filename)
	line = filecon.readline()
	sendPacket1 = recvPacket1 = sendPacket2 = recvPacket2 = 0
	while line:
		tokens = line.split(' ')
		if tokens[7] == "1":
			if tokens[2] == "0" and tokens[0] == "-":
				sendPacket1 = sendPacket1+1
			if tokens[0] == "r" and tokens[3] == '0'
				recvPacket1 = recvPacket1 + 1

		elif tokens[7] == "2":
			if tokens[2] == "4" and tokens[0] == "-":
				sendPacket2 = sendPacket2 + 1
			if tokens[0] == "r" and tokens[3] == '4'
				recvPacket2 = recvPacket2 + 1
	dr1 = 0 if sendNum1 == 0 else float(sendPacket1 - recvPacket1) / float(sendPacket1)
    dr2 = 0 if sendNum2 == 0 else float(sendPacket2 - recvPacket2) / float(sendPacket2)
    return str(dr1) + '\t' + str(dr2)



def calLatency(TCPType, CBRrate):
	filename = TCPType + "_" + str(CBRRate) + ".tr"
	filecon = open(filename)
	line = filecon.readline()
	starttime1 = {}
    endtime1 = {}
    starttime2 = {}
    endtime2 = {}
    totalduration1 = totalduration2 = 0.0
    totalpacket1 = totalpacket2 = 0
    while line:
    	tokens = line.split(' ')
    	if tokens[7] == "1":
    		if  tokens[2] == "0" and tokens[0] == "+":
                starttime1.update({tokens[10]: tokens[1]})
            if  tokens[2] == "0" and tokens[0] == "r":
                endtime1.update({tokens[10]: tokens[1]})
        if tokens[7] == "2":
    		if  tokens[2] == "0" and tokens[0] == "+":
                starttime2.update({tokens[10]: tokens[1]})
            if  tokens[2] == "0" and tokens[0] == "r":
                endtime2.update({tokens[10]: tokens[1]})

    packets = {x for x in start_time1.viewkeys() if x in end_time1.viewkeys()}
    for i in packets:
        start = start_time1[i]
        end = end_time1[i]
        duration = end - start
        if (duration > 0):
            total_duration1 += duration
            total_packet1 += 1
    packets = {x for x in start_time2.viewkeys() if x in end_time2.viewkeys()}
    for i in packets:
        start = start_time2[i]
        end = end_time2[i]
        duration = end - start
        if duration > 0:
            total_duration2 += duration
            total_packet2 += 1

    delay1 = 0 if total_packet1 == 0 else total_duration1 / total_packet1 * 1000
    delay2 = 0 if total_packet2 == 0 else total_duration2 / total_packet2 * 1000

    return str(delay1) + '\t' + str(delay2)



Reno_Reno_throughput = open('exp2_Reno_Reno_throughput.dat', 'w')
Reno_Reno_droprate = open('exp2_Reno_Reno_droprate.dat', 'w')
Reno_Reno_latency = open('exp2_Reno_Reno_latency.dat', 'w')
NewReno_Reno_throughput = open('exp2_NewReno_Reno_throughput.dat', 'w')
NewReno_Reno_droprate = open('exp2_NewReno_Reno_droprate.dat', 'w')
NewReno_Reno_latency = open('exp2_NewReno_Reno_latency.dat', 'w')
Vegas_Vegas_throughput = open('exp2_Vegas_Vegas_throughput.dat', 'w')
Vegas_Vegas_droprate = open('exp2_Vegas_Vegas_droprate.dat', 'w')
Vegas_Vegas_latency = open('exp2_Vegas_Vegas_latency.dat', 'w')
NewReno_Vegas_throughput = open('exp2_NewReno_Vegas_throughput.dat', 'w')
NewReno_Vegas_droprate = open('exp2_NewReno_Vegas_droprate.dat', 'w')
NewReno_Vegas_latency = open('exp2_NewReno_Vegas_latency.dat', 'w')
for CBRrate in range(1,10):
	TCPType = 'Reno_Reno'
	Reno_Reno_throughput.write(str(CBRrate) + '\t' + calThroughput(TCPType, CBRrate) + '\n')
    Reno_Reno_droprate.write(str(CBRrate) + '\t' + calDropRate(TCPType, CBRrate) + '\n')
    Reno_Reno_latency.write(str(CBRrate) + '\t' + latency(TCPType, CBRrate) + '\n')
    TCPType = 'NewReno_Reno':
    NewReno_Reno_throughput.write(str(CBRrate) + '\t' + calThroughput(TCPType, CBRrate) + '\n')
    NewReno_Reno_droprate.write(str(CBRrate) + '\t' + calDropRate(TCPType, CBRrate) + '\n')
    NewReno_Reno_latency.write(str(CBRrate) + '\t' + latency(TCPType, CBRrate) + '\n')
    TCPType = "Vegas_Vegas"
    Vegas_Vegas_throughput.write(str(CBRrate) + '\t' + calThroughput(TCPType, CBRrate) + '\n')
    Vegas_Vegas_droprate.write(str(CBRrate) + '\t' + calDropRate(TCPType, CBRrate) + '\n')
    Vegas_Vegas_latency.write(str(CBRrate) + '\t' + latency(TCPType, CBRrate) + '\n')
	TCPType = 'NewReno_Vegas'
    NewReno_Vegas_throughput.write(str(CBRrate) + '\t' + calThroughput(TCPType, CBRrate) + '\n')
    NewReno_Vegas_droprate.write(str(CBRrate) + '\t' + calDropRate(TCPType, CBRrate) + '\n')
    NewReno_Vegas_latency.write(str(CBRrate) + '\t' + latency(TCPType, CBRrate) + '\n')

Reno_Reno_droprate.close()
Reno_Reno_latency.close()
NewReno_Reno_throughput.close()
NewReno_Reno_droprate.close()
NewReno_Reno_latency.close()
Vegas_Vegas_throughput.close()
Vegas_Vegas_droprate.close()
Vegas_Vegas_latency.close()
NewReno_Vegas_throughput.close()
NewReno_Vegas_droprate.close()
NewReno_Vegas_latency.close()