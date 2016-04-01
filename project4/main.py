import HTTP
import os
import sys


#set the iptables
os.system('sudo iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP')

# for TEST
#url = "http://david.choffnes.com/classes/cs4700sp16/2MB.log"
#url = "http://david.choffnes.com/"
#url = "http://david.choffnes.com/classes/cs4700sp16/10MB.log"

if len(sys.argv)<2:
	print "You need input target url"
	sys.exit(0)
url = sys.argv[1]
Request = HTTP.HTTPRequest(url)
Request.sendGetRequest()

