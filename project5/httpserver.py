from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urllib
import urllib2
import sys
import getopt



class HTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # if not in cache:
        url = "http://" + origin + ":8080" + self.path
        data = ""
        try:
            response = urllib2.urlopen(url)
            data = response.read()
        except urllib2.HTTPError as e:
            self.send_error(e.code,e.message)
        except urllib2.URLError as e:
            self.send_error(e.message)
        except Exception as e:
            self.send_error(e.message)
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write(data)

if __name__ == '__main__':
    try:
        port = int(sys.argv[4])
        origin = sys.argv[2]
    except Exception:
        print 'You need input port and url. Exiting Program.'
        sys.exit()

    server = HTTPServer(('',port),HTTPHandler)
    server.serve_forever()

