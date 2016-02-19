#Create a simulator object
set ns [new Simulator]

#Open the trace file (before you start the experiment!)
set tf [open my_experiment1_output.tr w]
$ns trace-all $tf


#Define a 'finish' procedure
proc finish {} {
        global ns nf
        $ns flush-trace
        #Close the trace file
        close $tf
        #Execute python on the trace file
        exec python my_experiment1_output.tr &
        exit 0
}



#Create six nodes
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]
set n6 [$ns node]

#Create links between the nodes
$ns duplex-link $n1 $n2 10Mb 10ms DropTail
$ns duplex-link $n5 $n2 10Mb 10ms DropTail
$ns duplex-link $n2 $n3 10Mb 10ms DropTail
$ns duplex-link $n3 $n4 10Mb 10ms DropTail
$ns duplex-link $n6 $n6 10Mb 10ms DropTail


#Create a UDP agent and attach it to node n2
set udp0 [new Agent/UDP]
$ns attach-agent $n2 $udp0


#Setup a TCP connection
set tcp0 [new Agent/TCP]
$tcp set class_ 2
$ns attach-agent $n1 $tcp0

set sink [new Agent/TCPSink]
$ns attach-agent $n4 $sink
$ns connect $tcp0 $sink0
$tcp set fid_ 1

# Create a CBR traffic source and attach it to udp0
set cbr0 [new Application/Traffic/CBR]
$cbr0 set packetSize_ 500
$cbr0 set interval_ 0.005
$cbr0 attach-agent $udp0




#Create a sink and attach it to n3
set null0 [new Agent/Null] 
$ns attach-agent $n3 $null0

#connect each other
$ns connect $udp0 $null0

$ns at 0.5 "$cbr0 start"
$ns at 4.5 "$cbr0 stop"



#$ns at 5.0 "finish"


$ns run

# Close the trace file (after you finish the experiment!)
close $tf



