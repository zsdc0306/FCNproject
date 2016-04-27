from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urllib
import urllib2
import sys
import getopt
import urlparse
import commands
import re
import cache
import gzip
import zlib
import threading

class HTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # use url/doping to request the RTT between the replica and client
        if '/doping' in self.path:
            self.do_ping()
        else:
            httpcache = cache.httpcache()
            hit = httpcache.get(self.path)
            # if not in cache:
            if hit == -1:
                data = self.get_from_origin()
                if data != "":
                    print "cache"
                    httpcache.set(self.path, data)
            else:
                data = httpcache.get(self.path)
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                # self.send_header('Content-Encoding', "compress, gzip")
                self.end_headers()
                self.wfile.write(data)

    def get_from_origin(self):
        print "get page from origin server"
        url = "http://" + origin + ":8080" + self.path
        data = ""
        try:
            response = urllib2.urlopen(url)
            data = response.read()
        except urllib2.HTTPError as e:
            self.send_error(e.code, e.message)
        except urllib2.URLError as e:
            self.send_error(e.message)
        except Exception as e:
            self.send_error(e.message)
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        #self.send_header('Content-Encoding', "compress, gzip")
        self.end_headers()
        self.wfile.write(data)
        return data



    def do_ping(self):
        path = urlparse.urlparse(self.path)
        client_address = urlparse.parse_qs(path.query)['clientaddr'][0]
        print "cliant addr:" + client_address
        rtt = self.ping(client_address)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(rtt)

    def ping(self, client_addr):
        result = commands.getoutput('/usr/bin/scamper -c "ping -c 1" -i ' + client_addr)
        # patternstr = "time=(.*?) ms\n" # match the rtt
        # pattern = re.compile(patternstr)
        # time = re.findall(pattern, result)[0]
        # if time == '':
        #     time = "inf"
        # # use -1 for unreachable
        # print "RTT" + time
        # return time
        time = result.split('\n')[1].split()[-2].split('=')[-1]
        if time == 'statistics':
            time = 2000
        # print RTT
        return time


class prefecthThread(threading.Thread):
    def __init__(self, tar_host, tar_port, client_addr, lock=threading.Lock()):
        threading.Thread.__init__(self)

    def run(self):
        path = "/wiki/Main_Page"
        url = "http://" + origin + ":8080"+ path
        urllib2.urlopen(url)




if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "p:o:")
    port = 0
    try:
        for op, value in opts:
            if op == "-p":
                port = int(value)
            if op == "-o":
                origin = value
    except Exception as e:
        print "ERROR:" + e.message
        sys.exit(0)


    server = HTTPServer(('',port),HTTPHandler)
    server.serve_forever()

