import urllib2
import re
import HTMLParser
import Queue
import time
import gzip
import os

parser = HTMLParser.HTMLParser()
origin = "ec2-54-88-98-7.compute-1.amazonaws.com"
replica = ""
path = "/wiki/Portal:Contents"
url = "http://" + origin + ":8080" + path
size = 6*1024*1024
VisitedUrl = []
Url_Q = Queue.Queue()
Url_Q.put(url)
start_time = time.time()
while size>0 or time.time() - start_time > 20*60:
    url = Url_Q.get()
    if url not in VisitedUrl:
        try:
            response = urllib2.urlopen(url)
            data = response.read()
            if data:
                with gzip.open("temp", 'wb') as f:
                    f.write(data)
                size_com = os.path.getsize("temp")
                size -= size_com
                os.remove("temp")
            pattern_str = '<a href="(.*?)" '
            pattern = re.compile(pattern_str)
            urls = re.findall(pattern, data)
            for url in urls:
                decode_url = str(parser.unescape(url))
                fetch_url = "http://ec2-54-85-32-37.compute-1.amazonaws.com:50031" + decode_url
                if (fetch_url not in VisitedUrl):
                    Url_Q.put(fetch_url)
        except:
            pass
    else:
        continue

# try:
#     response = urllib2.urlopen(url)
#     data = response.read()
#     pattern_str = '<a href="(.*?)" '
#     pattern = re.compile(pattern_str)
#     urls = re.findall(pattern, data)
#     for url in urls:
#         decode_url = str(parser.unescape(url))
#         fetch_url = "http://ec2-54-85-32-37.compute-1.amazonaws.com:50031"+decode_url
#         try:
#             data = urllib2.urlopen(fetch_url)
#             print fetch_url + ": DONE"
#         except:
#             print fetch_url + ": ERROR"
# except Exception as e:
#     sys.exit(0)
