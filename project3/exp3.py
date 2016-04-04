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

def calThroughput(TCPType, QueueType):
    timescape = 0.5
    time = 0.0
	startTime1 = 0
	startTime2 = 0
	endTime1 = 0
	endTime2 = 0
	filename = TCPType + "-" + str(QueueType) + ".tr"
    outfile = 'ep3_' + TCPType + '_' + QueueType +'_throughput.dat'
	filecon = open(filename)
	throughput1 = 0.0
	throughput2 = 0.0
	line = filecon.readline()
    output= ""
	while line:
		tokens = line.split(' ')
		if tokens[7] == "1":
			if tokens[2] == "0" and tokens[0] == "+":
				startTime1 = float(tokens[1])
			if tokens[0] == "r":
				packetRecv1 += tokens[5] * 8
        if float(tokens[1]) - time > timescape:
            throughput1 = packetRecv1/timescape / (1024*1024)
            throughput2 = packetRecv2/timescape / (1024*1024)
            output += (str(time) + '\t' + str(throughput1) + '\t' + str(throughput2))
            output += "\n"
            outfile.write(output)
            time += timescape
    line = filecon.readline() 
    return throughput1 + "\t" + throughput2



def calLatency(TCPType, QueueType):
	filename = TCPType + "_" + str(CBRRate) + ".tr"
	filecon = open(filename)
	line = filecon.readline()
	starttime1 = {}
    endtime1 = {}
    starttime2 = {}
    endtime2 = {}
    totalduration1 = totalduration2 = 0.0
    totalpacket1 = totalpacket2 = 0
    time = 0.0
    outfile = 'ep3_' + TCPType + '_' + QueueType + '_latency.dat'
    while line:
    	tokens = line.split(' ')
    	if tokens[7] == "0":
    		if  tokens[2] == "0" and tokens[0] == "+":
                starttime1.update({tokens[10]: tokens[1]})
            if  tokens[2] == "0" and tokens[0] == "r":
                endtime1.update({tokens[10]: tokens[1]})
        if tokens[7] == "1":
    		if  tokens[2] == "0" and tokens[0] == "+":
                starttime2.update({tokens[10]: tokens[1]})
            if  tokens[2] == "0" and tokens[0] == "r":
                endtime2.update({tokens[10]: tokens[1]})

        if float(tokens[1]) - time > timescape:
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
            output = str(time) + "\t" + str(delay1) + "\t" +str(delay2) 
            output += "\n"
            outfile.write(output)
            time += timescape
        else:
            continue


    line = filecon.readline()   


    return str(delay1) + '\t' + str(delay2)


Reno_DropTail
Reno_RED
SACK_DropTail
SACK_RED

Reno_DropTail_throughput = open('exp3_Reno_DropTail_throughput.dat', 'w')
Reno_DropTail_latency = open('exp3_Reno_DropTail_latency.dat', 'w')
Reno_RED_throughput = open('exp3_Reno_RED_throughput.dat', 'w')
Reno_RED_latency = open('exp3_Reno_RED_latency.dat', 'w')
SACK_DropTail_throughput = open('exp3_SACK_DropTail_throughput.dat', 'w')
SACK_DropTail_latency = open('exp3_SACK_DropTail_latency.dat', 'w')
SACK_RED_throughput = open('exp3_SACK_RED_throughput.dat', 'w')
SACK_RED_latency = open('exp3_SACK_RED_throughput.dat', 'w')

TCPTypes = ['Reno', 'SACK']
QueueTypes = ['DropTail', 'RED']

for TCPType in TCPTypes:
    for QueueType in QueueTypes:
        calThroughput(TCPType, QueueType)
        calLatency(TCPType,QueueType)







