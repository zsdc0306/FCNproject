import socket
import urlparse
import commands
import connection
import _random
import sys
import re

#dstIP = "216.97.236.245"

CRLF = "\r\n"


class HTTPRequest:
    """class of the packet, including TCPHeader, IPHeader"""
    def __init__(self, url):
        self.urlStr = url
        self.url = urlparse.urlparse(self.urlStr)
        self.host = self.url.netloc
        self.path = self.url.path
        self.dstPort = 80
        self.dstIP = socket.gethostbyname(self.host)
        self.requestContent = ""


    def sendGetRequest(self):
        con = connection.Ccnnection(self.dstIP,self.dstPort)
        con.setTCPConnection()
        requestData = self.get()
        con.setRequestPack(requestData)
        con.startTransmit()
        data = con.recvedPackCon
        self.processHTML(data)

    # cut the HTML response header
    def processHTML(self,content):
        HTMLHeaderIndex = content.find('\r\n\r\n')
        HTMLResponseHeader = content[:HTMLHeaderIndex]
        if self.isChunk(HTMLResponseHeader):
            HTMLContent = content[HTMLHeaderIndex+2:]
        else:
            HTMLContent = content[HTMLHeaderIndex+4:]
        if HTMLResponseHeader.find("HTTP/1.1 200 OK") == -1:
            print "HTTP error"
            sys.exit()
        else:
            if self.isChunk(HTMLResponseHeader):
                HTMLContent = self.processChunk(HTMLContent)
            self.writeToFile(HTMLContent)

    # chunk flag is show as \r\nxxx\r\n, find it and replace it for ""
    def processChunk(self, data):
        patternstr = "\r\n(.*)\r\n"
        pattern = re.compile(patternstr)
        chunkFlag = re.findall(pattern, data)
        for flag in chunkFlag:
            if flag == "0":
                flagstr = "\r\n" + flag + "\r\n\r\n"                                            # the last flag is 0 and it is end with \r\n0\r\n\r\n
            else:
                flagstr = "\r\n" + flag + "\r\n"
            data = data.replace(flagstr,"")
        return data

    # to check whether it is chunk encodeing
    def isChunk(self,header):
        if "Transfer-Encoding: chunked" in header:
            return 1
        else:
            return 0

    def get(self):
        host = self.host
        path = self.path
        if path == '':
            path = '/'
        HTTP_Protocol = 'GET '+path+' HTTP/1.1'
        Request_Header = [
            HTTP_Protocol,
            "Host: "+host,
            "Connection: keep-alive",
            "Cache-Control: max-age=0",
            "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Upgrade-Insecure-Requests: 1",
            "DNT: 1",
            "Accept-Language: en-US,en;q=0.8,zh-CN;q=0.6",
            "",
            "",
        ]
        Request = CRLF.join(Request_Header)
        self.requestContent = Request
        return Request

    def writeToFile(self,content):
        path = self.path
        if path == '' or path == '/':
            filename = 'index.html'
        else:
            filename = path.split('/')[-1]

        targetFile = open(filename,'w')
        targetFile.write(content)
        print "writing done"
