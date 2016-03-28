import socket
import re



def RecvData(sock):
	Response =''
	ResponseHeader = sock.recv(4096)
	Response += ResponseHeader
	if isChunk(Response):
		if "\r\n0\r\n" in Response:
			return Response
		while 1:
			tmp = str(sock.recv(4096))
			if (tmp[0] == "0") or ("\n0\r\n" in tmp):
				break
			else:
				Response += tmp
		return Response
	elif "Content-Length:" in Response:
		content_pos = ResponseHeader.find("\r\n\r\n")+4
		content_len_rev = len(ResponseHeader[content_pos:])
		content_len = ResponseDatalength(ResponseHeader)
		length = content_len - content_len_rev
		if(length == 0):
			return Response
		while length != 0:
			tmp = sock.recv(4096)
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