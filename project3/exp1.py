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

def calcThroughput(TCPType, CBRRate):
    filename = TCPType + "_"+ str(CBRRate) + ".tr"
    fileopen = open(filename)
    line = fileopen.readline()

    while line:
        tokens = line.split(' ')
        if tokens[7] == "1":
            if tokens[2] == "0" and tokens[0] == "+":
                startTime = float(tokens[1])
            if tokens[0] == "r":
                packetRecv += tokens[5] * 8
                endTime = float(tokens[1])
        line = fileopen.readline()
    return packetRecv/(endTime - startTime)/(1024 * 1024)

def calcDroprate(TCPType, CBRRate):
    filename = TCPType + "_" + str(CBRRate) + ".tr"
    fileopen = open (filename)
    line = fileopen.readline()
    send_packets = 0
    recv_packets = 0
    while line:
        tokens = line.split(' ')
        if tokens[7] == "1":
            if tokens[2] == "0" and tokens[0] == "-"
                send_packets += 1
            if tokens[2] == "0" and tokens[0] == "r" and tokens[4] == "ack"
                recv_packets += 1
        line = fileopen.readline()
    if send_packets == 0:
        return 0
    drop_rate = float(send_packets - recv_packets) / float(send_packets) * 100
    return droprate

def calcLatency(TCPType, CBRRate):
    filename = TCPType + "_" + str(CBRRate) + ".tr"
    fileopen = open(filename)
    line = fileopen.readline()
    starttime = {}
    endtime = {}
    totalduration = 0.0
    totalpackets = 0
    while line:
        if tokens[7] == "1":
            if tokens[2] == "0" and tokens[0] == "+":
                starttime.update({tokens[10]:tokens[1]})
            if tokens[2] == "0" and tokens[0] == "r":
                endtime.update({tokens[10]:tokens[1]})
        line = fileopen.readline()
    packets = {x for x in starttime.viewkeys() if x in endtime.viewkeys()}
    for i in packets:
        start = starttime[i]
        end = end_time[i]
        duration = end - start
        if (duration > 0):
            total_duration += duration
            totalpackets += 1
    delay = 0 
    if total_packets == 0:
        return 0
    return total_duration / total_packets * 1000 

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
