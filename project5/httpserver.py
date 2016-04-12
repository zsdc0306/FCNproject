from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urllib
import urllib2
import sys


class HTTPHandler(BaseHTTPRequestHandler):
    def __init__(self, origin, cache, *args):
        self.origin = origin
        BaseHTTPRequestHandler.__init__(self, *args)


    def do_GET(self):
        # if not in cache:
        url = "http://" + self.origin + ":8080" + self.path
        try:
            response = urllib2.urlopen(url)
            data = response.read()
        except urllib2.HTTPError as e:
            self.send_error(e.code,e.message)
        except urllib2.URLError as e:
            self.send_error(e.message)
        except Exception as e:
            self.send_error(e.message)

try:
    port = sys.argv[4]
    origin = int(sys.argv[2])
except Exception:
    print 'You need input port and url. Exiting Program.'
    sys.exit()

server = HTTPServer(('',port),HTTPHandler)
server.serve_forever()

