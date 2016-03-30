import socket
import re
from connection import recvAck
import urlparse




def RecvData(sendsock, recvsock):
    Response =''
    ResponseHeader = recvAck(sendsock,recvsock)
    Response += ResponseHeader
    if isChunk(Response):
        if "\r\n0\r\n" in Response:
            print "!$@$@$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
            return Response
        while 1:
            tmp = str(recvAck(sendsock,recvsock))
            if (tmp[0] == "0") or ("\n0\r\n" in tmp):
                print "HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH"
                break
            else:
                Response += tmp
                print "tmp" + tmp
        return Response
    elif "Content-Length:" in Response:
        content_pos = ResponseHeader.find("\r\n\r\n")+4
        content_len_rev = len(ResponseHeader[content_pos:])
        content_len = ResponseDatalength(ResponseHeader)
        length = content_len - content_len_rev
        if(length == 0):
            return Response
        while length != 0:
            tmp = recvAck(sendsock,recvsock)
            Response += tmp
            length -= len(tmp)
        return Response
    else:
        return ''

def isChunk(header):
    if "Transfer-Encoding: chunked" in header:
        return 1
    else:
        return 0


def ResponseDatalength(header):
    patternstr = "Content-Length: (.*?)\r\n"
    pattern = re.compile(patternstr)
    datalength = re.findall(pattern, header)
    return int(datalength[0])




CRLF = "\r\n"
def get(url):
    url = urlparse.urlparse(url)
    host = url.netloc
    path = url.path
    if url.path == '':
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
    return Request

