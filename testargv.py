import sys
import getopt

print sys.argv[1:],sys.argv[1],sys.argv[2]

opts,args = getopt.getopt(sys.argv[1:22],"p:s")

for op,value in opts:
    if op=='-p':
        print "port:"+ value

