import collections
import threading
import os
import json
import gzip
import hashlib
import sys

class cache:
    lock = threading.Lock()
    def __init__(self, cachename,cache_size = 8 * 1024 * 1024):
        self.cache = collections.OrderedDict()
        # self.cache_file = open("cache.json", 'rw')
        self.cache_size = cache_size
        self.cache_name = cachename


    def set(self, key, value):
        with cache.lock:
            try:
                self.cache.pop(key)
            except KeyError:
                if len(self.cache) >= self.cache_size:
                    self.cache.popitem(last=False)
            self.cache[key] = value
            self.writedown()

    def get(self, key):
        with cache.lock:
            try:
                self.load()
                value = self.cache.pop(key)
                self.cache[key] = value
                return value
            except KeyError:
                return -1

    def writedown(self):
        with cache.lock:
            with open(self.cache_name, 'wb') as f:
                f.write(json.dumps(self.cache))

    def load(self):
        with cache.lock:
            if self.cache_name not in os.listdir("."):
                os.system("touch " + self.cache_name)
                with open(self.cache_name, 'wb') as f:
                    f.write('{}')
            with open(self.cache_name, 'rb') as f:
                content = f.read()
            self.cache = json.loads(content)

class httpcache:
    lock = threading.Lock()
    def __init__(self, cachename = "cache", cache_size=10 * 1024 * 1024 - 500 * 1024):
        self.pagelist = collections.OrderedDict()
        self.pagelist_name = "pagelist.json"
        self.dirname = cachename
        self.cache_size = cache_size
        self.create_dir()

    def create_dir(self):
        if not os.path.exists(self.dirname):
            os.mkdir(self.dirname)
        else:
            pass

    def isExist(self,path_md5, dir):
        if path_md5 in self.pagelist:
            if os.path.isfile(dir):
                return 1
            else:
                self.pagelist.pop(path_md5)
                return 0
        else:
            return 0

    def is_full(self, content):
        size = self.cache_size
        curr_size = sum(os.path.getsize(self.dirname + "/" + f) for f in os.listdir(self.dirname) if os.path.isfile(self.dirname + "/" + f))
        return (curr_size + sys.getsizeof(content)) < size


# def set(self, key, value):
#     with cache.lock:
#         try:
#             self.cache.pop(key)
#         except KeyError:
#             if len(self.cache) >= self.cache_size:
#                 self.cache.popitem(last=False)
#         self.cache[key] = value
#         self.writedown()

    def set(self, path, content):
        path_md5 = self.md5path(path)
        dir = self.dirname + '/' + path
        self.pagelist_load()
        try:
            self.pagelist.pop(path_md5, dir)
            self.content_pop(path_md5, dir)
        except KeyError:
            if self.is_full(content):
                self.pagelist.popitem(last=False)
        try:
            self.writedown(dir ,content)
            self.pagelist[path_md5] = self.dirname + '/' + path
            self.pagelist_writedown()
        except IOError as e:
            print "http cache error: " + e.message


    def writedown(self, dir, content):
        with gzip.open(dir,'wb') as f:
            f.write(content)

    def content_pop(self, path_md5, dir):
        if self.isExist(path_md5,dir):
            os.remove(dir)
        else:
            pass

    def get(self, path):
        path_md5 = self.md5path(path)
        dir = self.dirname + '/' + path
        self.pagelist_load()
        try:
            dir = self.pagelist.pop(path_md5)
            self.pagelist[path_md5] = dir
            try:
                with gzip.open(dir,"rb") as f:
                    content = f.read()
                    return content
            except:
                self.pagelist.pop(path_md5)
                self.pagelist_writedown()
                return -1
        except KeyError:
            return -1


    def md5path(self, path):
        hashentity = hashlib.md5()
        hashentity.update(path)
        return hashentity.hexdigest()


    def pagelist_writedown(self):
        with open(self.pagelist_name, 'wb') as f:
            f.write(json.dumps(self.pagelist))


    def pagelist_load(self):
        if not os.path.isfile(self.pagelist_name):
            with open(self.pagelist_name, 'wb') as f:
                f.write('{}')
        else:
            with open(self.pagelist_name, 'rb') as f:
                content = f.read()
            self.pagelist = json.loads(content)

