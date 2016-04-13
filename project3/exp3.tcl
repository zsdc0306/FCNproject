# Create a Simulator object
set ns [new Simulator]

$ns color 0 Blue
$ns color 1 Red

# TCP var
set tcpType [lindex $argv 0]
# Queue var
set queueType [lindex $argv 1]

# Open the trace file
set tf [open ${tcpType}-${queueType}_output.tr w]
$ns trace-all $tf

# Define a 'finish' procedure
proc finish {} {
	global ns tf
	$ns flush-trace
	close $tf
	exit 0
}

# create 6 nodes
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]
set n6 [$ns node]

#create links between the nodes
if {$queueType eq "DropTail"} {
	$ns duplex-link $n1 $n2 10Mb 10ms DropTail
	$ns duplex-link $n2 $n3 10Mb 10ms DropTail
	$ns duplex-link $n5 $n2 10Mb 10ms DropTail
	$ns duplex-link $n4 $n3 10Mb 10ms DropTail
	$ns duplex-link $n6 $n3 10Mb 10ms DropTail
} elseif {$queueType eq "RED"} {
	$ns duplex-link $n1 $n2 10Mb 10ms RED
	$ns duplex-link $n2 $n3 10Mb 10ms RED
	$ns duplex-link $n5 $n2 10Mb 10ms RED
	$ns duplex-link $n4 $n3 10Mb 10ms RED
	$ns duplex-link $n6 $n3 10Mb 10ms RED
}

#set queue size
$ns queue-limit	$n1 $n2 10
$ns queue-limit	$n5 $n2 10
$ns queue-limit	$n2 $n3 10
$ns queue-limit	$n4 $n3 10
$ns queue-limit	$n6 $n3 10

#Setup a UDP connection
set udp [new Agent/UDP]
$ns attach-agent $n5 $udp
set null [new Agent/Null]
$ns attach-agent $n6 $null
$ns connect $udp $null




#Setup a CBR over UDP connection
set cbr0 [new Application/Traffic/CBR]
$cbr0 attach-agent $udp
$cbr0 set packetSize_ 500
$cbr0 set interval_ 0.005
$cbr0 set type_ CBR
$cbr0 set rate_ 7mb

#Setup a TCP conncection
if {$tcpType eq "Reno"} {
	set tcp [new Agent/TCP/Reno]
	set sink [new Agent/TCPSink]
} elseif {$tcpType eq "SACK"} {
	set tcp [new Agent/TCP/Sack1]
	set sink [new Agent/TCPSink/Sack1]
}

$tcp set class_ 1
$ns attach-agent $n1 $tcp
$ns attach-agent $n4 $sink
$ns connect $tcp $sink

#setup a FTP Application
set ftp [new Application/FTP]
$ftp attach-agent $tcp

#Schedule events for the CBR and FTP agents
$ns at 0.0 "$ftp start"
$ns at 3.0 "$cbr0 start"
$ns at 30.0 "$ftp stop"
$ns at 35.0 "$cbr0 stop"

#Call the finish procedure after  seconds of simulation time
$ns at 40.0 "finish"

#Run the simulation
$ns run
