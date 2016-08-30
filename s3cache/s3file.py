"""
Wrap a local file with code to copy the contents into and out of S3
"""
import os
from boto.s3.key import Key
from boto.exception import S3ResponseError
import s3cache.utils
from .exception import S3CacheBucketNotExistError, S3CacheIOError


class S3File(object):
    """Wrap a local file with code to copy the contents into and out of S3"""

    def __init__(self, mgr, path):
        """create and open a file using the cache manager, file path and mode
        """
        self.mgr = mgr
        self.path = path
        self.mode = None
        self.file = None
        # DELETE self.tmppath = os.path.join(mgr.tmpdir,
        #  s3cache.utils.mangle(path))
        self.tmppath = s3cache.utils.abspath(mgr.tmpdir, path)

    def remove_cached(self):
        """Remove locally-cached copy."""
        retv = True
        if os.path.exists(self.tmppath):
            try:
                os.remove(self.tmppath)
                self.log("removed local cache file(" + self.tmppath + ")")
            except OSError:
                retv = False
                self.log("problem removing local cache file(" +
                         self.tmppath + ")")
        return retv

    def remove(self):
        """Remove a file locally and from S3."""
        self.log("removing file")
        self.remove_cached()
        self.log("removing file from S3")
        retv = True
        try:
            k = Key(self.mgr.bucket, self.path)
            k.delete()
        except (S3ResponseError, ValueError) as err:
            retv = False
            self.log("Problem removing file: " + err)
        return retv

    def exists(self):
        """Determines if a file exists on S3"""
        retv = False
        try:
            k = Key(self.mgr.bucket, self.path)
            retv = k.exists()
        except S3ResponseError as err:
            retv = False
            self.log("Problem checking existence of file: " + err)
        return retv

    def cached(self):
        """Determines if files is cached locally, but without regard of
        whether it exists in S3.
        """
        return os.path.exists(self.tmppath)

    def open(self, mode):
        """Opens a file to read or write operations."""
        self._bucket_exists_()
        s3cache.utils.makedirs(self.tmppath)
        self.mode = mode
        if 'r' in self.mode or 'a' in self.mode:
            # opening an existing file, try to copy in from s3 if not in local
            # cache
            self.log("trying to open file")
            use_local_copy = self.mgr.caching
            if use_local_copy:
                if not os.path.exists(self.tmppath):
                    self.log(
                        "not found in local cache, attempting to load from S3")
                    use_local_copy = False
            if not use_local_copy:
                k = Key(self.mgr.bucket, self.path)
                try:
                    k.get_contents_to_filename(self.tmppath)
                    self.log("file located in S3, downloaded from S3 to cache")
                except S3ResponseError:
                    raise S3CacheIOError("//{0}/{1}"
                                         .format(self.mgr.bucket_name,
                                                 self.path))
            else:
                self.log("file found in local cache")
        else:
            self.log("opening new file in local cache for writing")
        # open the local file
        self.log("opening local cache file(" + self.tmppath + ")")
        self.file = open(self.tmppath, self.mode)

    def __getattr__(self, name):
        return S3File.Delegator(self.file, name)

    # pylint: disable=too-few-public-methods
    class Delegator(object):
        """utility class to delegate a call on this class to the local file
        """

        def __init__(self, target, name):
            self.target = target
            self.name = name

        def __call__(self, *args, **kwargs):
            method = self.target.__class__.__dict__[self.name]
            oargs = [self.target]
            oargs += args
            return method(*oargs, **kwargs)

    def close(self):
        """On closing the file, copy it back to s3 if it was opened for
        writing/appending.

        :rtype: int
        :return: the number of bytes written
        """
        self.log("closing local cache file(" + self.tmppath + ")")
        self.file.close()
        bytes_written = 0
        if 'w' in self.mode or 'a' in self.mode:
            self.log("writing updated cache file contents to S3")
            k = Key(self.mgr.bucket, self.path)
            try:
                bytes_written = k.set_contents_from_filename(self.tmppath)
            except AttributeError as err:
                self.log(str(err))
                raise
        if not self.mgr.caching:
            # remove the local copy if caching is turned off
            self.remove_cached()
        return bytes_written

    def log(self, msg):
        """Logger"""
        self.mgr.log("S3File(" + self.path + "): " + msg)

    def _bucket_exists_(self):
        """Internal sanity check"""
        self.mgr.connect()
        if not self.mgr.bucket_exists():
            raise S3CacheBucketNotExistError(self.mgr.bucket_name)
