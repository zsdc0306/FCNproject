import threading
import urllib2
import cache

replica_host_delay = {
    'ec2-54-85-32-37.compute-1.amazonaws.com':2000.0,
    'ec2-54-193-70-31.us-west-1.compute.amazonaws.com':2000.0,
    'ec2-52-38-67-246.us-west-2.compute.amazonaws.com':2000.0,
    'ec2-52-51-20-200.eu-west-1.compute.amazonaws.com':2000.0,
    'ec2-52-29-65-165.eu-central-1.compute.amazonaws.com':2000.0,
    'ec2-52-196-70-227.ap-northeast-1.compute.amazonaws.com':2000.0,
    'ec2-54-169-117-213.ap-southeast-1.compute.amazonaws.com':2000.0,
    'ec2-52-63-206-143.ap-southeast-2.compute.amazonaws.com':2000.0,
    'ec2-54-233-185-94.sa-east-1.compute.amazonaws.com':2000.0,
}

class TestRTTThread(threading.Thread):
    def __init__(self, tar_host,tar_port, client_addr, lock=threading.Lock()):
        threading.Thread.__init__(self)
        self.lock = lock
        self.tar_host = tar_host #replica host name
        self.tar_port = tar_port
        self.clent_addr = client_addr # ip of client

    def run(self):
        url = "http://" + self.tar_host+":" + str(self.tar_port) + "/doping?clientaddr=" + self.clent_addr
        try:
            testresponse = urllib2.urlopen(url)
            data = testresponse.read()
            print "response" + data
            key = self.tar_host
            val = float(data)
            with self.lock:
                replica_host_delay.update({key: val})
        except Exception as e:
            replica_host_delay[self.tar_host] = "2000"
            print "RTT Test error" + e.message

