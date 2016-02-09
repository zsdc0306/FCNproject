#! /usr/bin/python2.7

import re
import string
import socket
import sys
import urlparse


#config data
FakebookUrl = 'http://cs5700sp16.ccs.neu.edu/accounts/login/?next=/fakebook/'
Useragent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'

port = 80
CRLF = '\r\n'  #need to add to end of every line 
AcceptContent = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' 
Connection = 'keep-alive'


username = '001777115'
password = '9NXCJQNN'

if(len(sys.argv)>=1)
	username = argv[1]
	password = argv[2]

secretFlagMatch = '<h2 class=\'secret_flag\' style="color:red">FLAG: (.)</h2>'

def createsocket():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((host,80))
	sock.send(Request_Head)
#socket.setdefaulttimeout(10)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host,80))
sock.sendall(CRLF.join(Request_Head))
data = sock.recv(4096)

def get(sock, url):
	url = urlparse.urlparse(url)
	host = url.netloc
	if url.path == '':
		path = '/'
	path = url.path
	HTTP_Protocol = 'GET '+path+' HTTP/1.1'
	Request_Header = [
		HTTP_Protocol,
		"Host: "+host,
		"Connection: keep-alive",
		"Cache-Control: max-age=0",
		"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
		"Upgrade-Insecure-Requests: 1",
		"User-Agent: "+Useragent,
		"DNT: 1",
		"Accept-Language: en-US,en;q=0.8,zh-CN;q=0.6",
		"",
		"",
	]
	Request = CRLF.join(Request_Header)
	sock.sendall(Request)
	
	Response = sock.recv(4096)
	tmp = sock.recv(4096)
	while (tmp):
		Response = tmp + Response
		tmp = sock.recv(4096)

	return Response

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host,80))
get(sock,'http://cs5700sp16.ccs.neu.edu/accounts/login/?next=/fakebook/')

def post(sock, url, postdata):
	url = urlparse.urlparse(url)
	host = url.netloc
	if url.path == '':
		path = '/'
	path = url.path
	HTTP_Protocol = 'POST '+path+' HTTP/1.1'
	datalength = len(postdata)
	Request_Header = [
		HTTP_Protocol,
		"Host: "+host,
		"Connection: keep-alive",
		"Cache-Control: max-age=0",
		"Content-Length: " + datalength, 
		"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
		"Upgrade-Insecure-Requests: 1",
		"User-Agent: "+Useragent,
		"DNT: 1",
		"Accept-Language: en-US,en;q=0.8,zh-CN;q=0.6",
		"",
		"",
	]


Useragent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'
datalength = len(postdata)
Request_Header = [
	"POST /accounts/login/?next=/fakebook/ HTTP/1.1",
	"Host: cs5700sp16.ccs.neu.edu",
	"Connection: keep-alive",
	"User-Agent: "+Useragent,
	"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	"Accept-Language: en-US,en;q=0.8,zh-CN;q=0.6",
	"Content-Type: application/x-www-form-urlencoded",
	"Referer: http://cs5700sp16.ccs.neu.edu",
	"",
	"",
]

Request = "POST /accounts/login/?next=/fakebook/ HTTP/1.1\r\nHost: cs5700sp16.ccs.neu.edu\r\nConnection: keep-alive\r\n"



Request = CRLF.join(Request_Header) + postdata
sock.sendall(Request)
Response = sock.recv(4096)
"Content-Length: " + str(datalength),
"Cookie: csrftoken="+getcsrftoken(data)+"; sessionid="+getsessionid(data),
	"Cache-Control: max-age=0",
	"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	"Origin: http://cs5700sp16.ccs.neu.edu",
	"Upgrade-Insecure-Requests: 1",
	
	"DNT: 1",
	
"Referer: http://cs5700sp16.ccs.neu.edu/accounts/login/?next=/fakebook/",
sock = createSocket()
data = get(sock,'http://cs5700sp16.ccs.neu.edu/accounts/login/?next=/fakebook/')
postdata = 'username=001777115&password=9NXCJQNN&csrfmiddlewaretoken='+getcsrftoken(data)

+'&next=%2Ffakebook%2F'


data = get(createSocket(),'http://cs5700sp16.ccs.neu.edu/accounts/login/?next=/fakebook/')
def createSocket():
	host = "cs5700sp16.ccs.neu.edu"
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((host,80))
	return sock



sock.sendall(CRLF.join(Request_Header))
data = sock.recv(4096)

#login the fakefook
def login():
	



#check whether the url has been scanned
def isSeen(url):


#save the scanned url
def storeUrl(url):




#def match