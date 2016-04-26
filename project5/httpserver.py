from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urllib
import urllib2
import sys
import getopt
import urlparse
import commands
import re
import cache

class HTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        httpcache = cache.httpcache()
        hit = httpcache.get(self.path)
        if hit == -1:
            self.get_from_origin()

        # use url/doping to request the RTT between the replica and client
        if '/doping' in self.path:
            self.do_ping()
            return
        # if not in cache:


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
        self.end_headers()
        self.wfile.write(data)


    def do_ping(self):
        path = urlparse.urlparse(self.path)
        client_address = urlparse.parse_qs(path.query)['clientaddr'][0]
        print "cliant addr:" + client_address
        rtt = self.ping(client_address)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(rtt)

    def ping(self, client_addr):
        result = commands.getoutput('/usr/bin/scamper -c \'ping -c 1\' -i ' + client_addr)
        patternstr = "time=(.*?)ms" # match the rtt
        pattern = re.compile(patternstr)
        time = re.findall(pattern, result)[0]
        if time == '':
            time = "inf"
        # use -1 for unreachable
        print "RTT" + time
        return time



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

