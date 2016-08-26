import boto
import os
from s3file import s3file

class s3cache(object):

    # singleton instance
    instance = None

    # initialize the cache
    def __init__(self,tmpdir,bucket_name):
        self.bucket_name = bucket_name
        self.conn = None
        self.bucket = None
        self.tmpdir = tmpdir
        self.verbosity = False
        self.caching = True
        s3cache.instance = self
        
    # ensure that a connection to s3 exists
    def connect(self):
        if self.conn == None:
            try:
                self.conn = boto.connect_s3()
                self.bucket = self.conn.create_bucket(self.bucket_name)
            except:
                raise "Error - cannot connect to S3"
            
    # write a message to the log (if verbosity is on)
    def log(self,msg):
        if self.verbosity:
            print msg
            
    # remove a file
    def removePath(self,path):
        self.connect()
        s3f = s3file(s3cache.instance,path)
        s3f.remove()
                        
    # set verbosity on/off (default=off)
    @staticmethod
    def setVerbosity(verbosity):
        s3cache.instance.verbosity = verbosity
        
    # set local file caching on/off (default=on)
    @staticmethod
    def setCaching(caching):
        s3cache.instance.caching = caching

    # open a file in the cache and return a file-like object
    @staticmethod
    def open(path,mode):
        s3cache.instance.connect()
        s3f = s3file(s3cache.instance,path)
        s3f.open(mode)
        return s3f
        
    @staticmethod
    def remove(path):
        return s3cache.instance.removePath(path)
        
# Configuration
#
# create the singleton instance        

# define the local cache directory
local_cache_directory = "/tmp"
s3_bucket_name = "mccarroll.net.test"

s3cache(local_cache_directory,s3_bucket_name)
