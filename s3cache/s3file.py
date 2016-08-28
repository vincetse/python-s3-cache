import boto
from boto.s3.key import Key
import os

#
# wrap a local file with code to copy the contents into
# and out of S3
#


class s3file(object):

    # create and open a file using the cache manager, file path and mode
    def __init__(self, mgr, path):
        self.mgr = mgr
        self.path = path
        self.mode = None
        self.tmppath = os.path.join(mgr.tmpdir, self.mangle(path))

    def removeCache(self):
        # remove local cache copy
        if os.path.exists(self.tmppath):
            try:
                os.remove(self.tmppath)
                self.log("removed local cache file(" + self.tmppath + ")")
            except:
                self.log("problem removing local cache file(" +
                         self.tmppath + ")")
                pass

    def remove(self):
        self.log("removing file")
        self.removeCache()
        self.log("removing file from S3")
        k = Key(self.mgr.bucket)
        k.key = self.path
        try:
            k.delete()
        except:
            self.log("problem removing file")

    def open(self, mode):
        self.mode = mode
        if 'r' in self.mode or 'a' in self.mode:
            # opening an existing file, try to copy in from s3 if not in local
            # cache
            self.log("trying to open existing file")
            use_local_copy = self.mgr.caching
            if use_local_copy:
                if not os.path.exists(self.tmppath):
                    self.log(
                        "not found in local cache, attempting to load from S3")
                    use_local_copy = False
            if not use_local_copy:
                try:
                    k = Key(self.mgr.bucket)
                    k.key = self.path
                    k.get_contents_to_filename(self.tmppath)
                    self.log("file located in S3, downloaded from S3 to cache")
                except:
                    self.log("file not found in S3, opening new empty file "
                             "in local cache")
                    pass
            else:
                self.log("file found in local cache")
        else:
            self.log("opening new file in local cache for writing")
        # open the local file
        self.log("opening local cache file(" + self.tmppath + ")")
        self.file = open(self.tmppath, self.mode)

    # mangle the original file path to replace separators with underscores
    # and double up existing underscores
    def mangle(self, path):
        mangled_path = ''
        for c in path:
            if c == '/':
                mangled_path += '_'
            elif c == '_':
                mangled_path += '__'
            else:
                mangled_path += c
        return mangled_path

    def __getattr__(self, name):
        return s3file.delegator(self.file, name)

    # utility class to delegate
    # a call on this class to the local file
    class delegator(object):

        def __init__(self, target, name):
            self.target = target
            self.name = name

        def __call__(self, *args, **kwargs):
            method = self.target.__class__.__dict__[self.name]
            oargs = [self.target]
            oargs += args
            return method(*oargs, **kwargs)

    # on closing the file, copy it back to s3 if it was opened for
    # writing/appending
    def close(self):
        self.log("closing local cache file(" + self.tmppath + ")")
        self.file.close()
        if 'w' in self.mode or 'a' in self.mode:
            self.log("writing updated cache file contents to S3")
            try:
                k = Key(self.mgr.bucket)
                k.key = self.path
                k.set_contents_from_filename(self.tmppath)
                self.log("write complete")
            except:
                self.log("ERROR - write to S3 failed")

    def log(self, msg):
        self.mgr.log("s3file(" + self.path + "): " + msg)
