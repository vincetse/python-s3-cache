import boto
import os
from s3file import s3file


class s3cache(object):

    # initialize the cache
    def __init__(self, tmpdir, bucket_name,
                 host='s3.amazonaws.com', port=None, is_secure=True):
        self.bucket_name = bucket_name
        self.conn = None
        self.bucket = None
        self.tmpdir = tmpdir
        self.verbosity = False
        self.caching = True
        self.host = host
        self.port = port
        self.is_secure = is_secure

    # ensure that a connection to s3 exists
    def connect(self):
        if self.conn is None:
            try:
                self.conn = boto.connect_s3(
                    port=self.port, host=self.host, is_secure=self.is_secure)
            except:
                raise IOError("cannot connect to S3")

    # does the bucket exist?
    def bucketExists(self):
        self.connect()
        bucket = self.conn.lookup(self.bucket_name)
        return (bucket is not None)

    # create bucket
    def createBucket(self):
        if not self.bucketExists():
            self.bucket = self.conn.create_bucket(self.bucket_name)
        return (self.bucket is not None)

    # write a message to the log (if verbosity is on)
    def log(self, msg):
        if self.verbosity:
            print msg

    # remove a file
    def remove(self, path):
        self.connect()
        s3f = s3file(self, path)
        s3f.remove()

    # get local tmp directory
    def localCache(self):
        return self.tmpdir

    # set verbosity on/off (default=off)
    def setVerbosity(self, verbosity):
        self.verbosity = verbosity

    # set local file caching on/off (default=on)
    def setCaching(self, caching):
        self.caching = caching

    # open a file in the cache and return a file-like object
    def open(self, path, mode):
        self.connect()
        s3f = s3file(self, path)
        s3f.open(mode)
        return s3f
