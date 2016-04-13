# Create a Simulator object
set ns [new Simulator]

# TCP TCPVar1
set TCPVar1 [lindex $argv 0]
set TCPVar2 [lindex $argv 1]
# CBR rate
set rate [lindex $argv 2]

# Open the trace file
set tf [open ${TCPVar1}_${TCPVar2}_${rate}.tr w]
$ns trace-all $tf


# Define a 'finish' procedure
proc finish {} {
	global ns tf tcp
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
$ns duplex-link $n1 $n2 10Mb 10ms DropTail
$ns duplex-link $n5 $n2 10Mb 10ms DropTail
$ns duplex-link $n2 $n3 10Mb 10ms DropTail
$ns duplex-link $n4 $n3 10Mb 10ms DropTail
$ns duplex-link $n6 $n3 10Mb 10ms DropTail



#set the topology shape
$ns duplex-link-op $n1 $n2 orient right-down
$ns duplex-link-op $n2 $n3 orient right
$ns duplex-link-op $n5 $n2 orient right-up
$ns duplex-link-op $n3 $n4 orient right-up
$ns duplex-link-op $n3 $n6 orient right-down


#Setup a UDP connection
set udp0 [new Agent/UDP]
$ns attach-agent $n2 $udp0


#Setup a CBR over UDP connection
set cbr0 [new Application/Traffic/CBR]
$cbr0 attach-agent $udp
# change rate until tcp can reach its bottleneck
$cbr0 set rate_ ${rate}mb
$cbr0 set random_ false



set null [new Agent/Null]
$ns attach-agent $n3 $null
$ns connect $udp0 $null

# TODO:
#Agent/TCP - a “tahoe” TCP sender
#Agent/TCP/Reno - a “Reno” TCP sender
#Agent/TCP/Newreno - Reno with a modication
#Agent/TCP/Sack1 - TCP with selective repeat (follows RFC2018)
#Agent/TCP/Vegas - TCP Vegas
#Agent/TCP/Fack - Reno TCP with .forward acknowledgment.




#Setup a TCP conncection
if {$TCPVar1 eq "Reno"} {
	set tcp1 [new Agent/TCP/Reno]
} elseif {$TCPVar1 eq "NewReno"} {
	set tcp1 [new Agent/TCP/Newreno]
} elseif {$TCPVar1 eq "Vegas"} {
	set tcp1 [new Agent/TCP/Vegas]
}

$tcp1 set class_ 1
$ns attach-agent $n1 $tcp1
set sink1 [new Agent/TCPSink]
$ns attach-agent $n4 $sink1
$ns connect $tcp1 $sink1

if {$TCPVar2 eq "Reno"} {
	set tcp2 [new Agent/TCP/Reno]
} elseif {$TCPVar2 eq "Vegas"} {
	set tcp2 [new Agent/TCP/Vegas]
}

$tcp2 set class_ 2
$ns attach-agent $n5 $tcp2
set sink2 [new Agent/TCPSink]
$ns attach-agent $n6 $sink2
$ns connect $tcp2 $sink2

#setup a FTP Application
set ftp1 [new Application/FTP]
$ftp1 attach-agent $tcp1

set ftp2 [new Application/FTP]
$ftp2 attach-agent $tcp2

#Schedule events for the CBR and FTP agents
$ns at 0.0 "$cbr start"
$ns at 0.0 "$ftp1 start"
$ns at 0.0 "$ftp2 start"
$ns at 10.0 "$ftp2 stop"
$ns at 10.0 "$ftp1 stop"
$ns at 10.0 "$cbr stop"

#Call the finish procedure after  seconds of simulation time
$ns at 10.0 "finish"

#Run the simulation
$ns run
