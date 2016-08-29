"""
An AWS S3 local cache.
"""
import os
import boto
from .s3file import S3File


# pylint: disable=too-many-instance-attributes
class S3Cache(object):
    """Caches AWS S3 objects locally."""

    # initialize the cache
    # pylint: disable=too-many-arguments
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

    def connect(self):
        """Connect to AWS S3.  """

        if self.conn is None:
            try:
                self.conn = boto.connect_s3(
                    port=self.port, host=self.host, is_secure=self.is_secure)
            except:
                raise IOError("cannot connect to S3")

    def bucket_exists(self):
        """Checks for existence of bucket"""
        self.connect()
        bucket = self.conn.lookup(self.bucket_name)
        return bucket is not None

    def create_bucket(self):
        """Creates a bucket"""
        if not self.bucket_exists():
            self.bucket = self.conn.create_bucket(self.bucket_name)
        return self.bucket is not None

    def log(self, msg):
        """Write a message to the log (if verbosity is on)"""
        if self.verbosity:
            print msg

    def remove(self, path):
        """Removes a file."""
        self.connect()
        s3f = S3File(self, path)
        s3f.remove()

    def local_cache(self):
        """Gets the local cache directory"""
        return self.tmpdir

    def set_verbosity(self, verbosity):
        """Sets verbosity"""
        self.verbosity = verbosity

    def set_caching(self, caching):
        """Determines if we always go out to S3 or use local copy
        if it exists.  (default: on)
        """
        self.caching = caching

    def open(self, path, mode):
        """open a file in the cache and return a file-like object."""
        self.connect()
        s3f = S3File(self, path)
        s3f.open(mode)
        return s3f
