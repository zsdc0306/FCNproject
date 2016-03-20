#Create a simulator object
set ns [new Simulator]

#Open the trace file (before you start the experiment!)
# set tf [open my_experiment1_output.tr w]
# $ns trace-all $tf

$ns color 0 Blue
$ns color 1 Red


#get TCP type and bandwith from user
proc getval {argc argv} {
        global val
        lappend vallist r x y z
        #argc为参数的个数，argv为整条参数构成的字符串
        for {set i 0} {$i < $argc} {incr i} {
        #变量arg为argv的第i部分，以空格为分界
                set arg [lindex $argv $i]
                #略过无字符“-”的字符串，一般是用户键入的数字
                #string range $arg m n表示取字符串$arg的第m个字符到第n个字符
                if {[string range $arg 0 0] != "-"} continue
                set name [string range $arg 1 end]
                #更改预设变量（结点个数，半径，场景大小）
                set val($name) [lindex $argv [expr $i+1]]
        }

}





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

#Open the NAM trace file
set nf [open out.nam w]
set tf [open my_experiment1_output.tr w]
$ns namtrace-all $nf
$ns trace-all $tf


#Define a 'finish' procedure
proc nam_finish {} {
        global ns nf
        $ns flush-trace
        #Close the NAM trace file
        close $nf
        #Execute NAM on the trace file
        exec nam out.nam &
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
$ns duplex-link $n3 $n6 10Mb 10ms DropTail


#set the topology shape
$ns duplex-link-op $n1 $n2 orient right-down
$ns duplex-link-op $n2 $n3 orient right
$ns duplex-link-op $n5 $n2 orient right-up
$ns duplex-link-op $n3 $n4 orient right-up
$ns duplex-link-op $n3 $n6 orient right-down


#Create a UDP agent and attach it to node n2
set udp0 [new Agent/UDP]
$ns attach-agent $n2 $udp0


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






#Setup a Tahoe TCP connection
set tcp [new Agent/TCP]
$ns attach-agent $n1 $tcp

#Setup a FTP over TCP connection
set ftp [new Application/FTP]
$ftp attach-agent $tcp
$ftp set type_ FTP


set sink [new Agent/TCPSink]
$ns attach-agent $n4 $sink
$ns connect $tcp $sink
$tcp set fid_ 1






$ns at 0.5 "$cbr0 start"
$ns at 1.0 "$ftp start"
$ns at 4.0 "$ftp stop"
$ns at 4.5 "$cbr0 stop"



$ns at 5.0 "nam_finish"


$ns run

# Close the trace file (after you finish the experiment!)
close $tf



