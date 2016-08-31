from nose.tools import *
from nose import with_setup
import unittest
import os
import shutil
import tempfile
import uuid
from s3cache import S3Cache
from s3cache.exception import *


def _read_file(filename):
    content = ""
    with open(filename, 'r') as content_file:
        content = content_file.read()
    return content


class TestS3Cache(unittest.TestCase):

    def setUp(self):
        self.cleanup_dirs = []

    def tearDown(self):
        for d in self.cleanup_dirs:
            shutil.rmtree(d)

    def cleanup(self, d):
        self.cleanup_dirs.append(d)

    def bucketFactory(self, create=True):
        bucket_name = str(uuid.uuid4())
        local_cache = tempfile.mkdtemp()
        self.cleanup(local_cache)
        self.assertTrue(os.path.exists(local_cache))
        endpoint = os.environ['S3_ENDPOINT']
        port = int(os.environ['S3_PORT'])
        s3 = S3Cache(local_cache, bucket_name, port=port,
                     is_secure=False, host=endpoint)
        if create:
            s3.create_bucket()
            self.assertTrue(s3.bucket_exists())
            s3.set_verbosity(True)
            s3.set_caching(True)
        return s3

    @raises(S3CacheConnectError)
    def testS3ConnectionTimeout(self):
        bucket_name = str(uuid.uuid4())
        local_cache = tempfile.mkdtemp()
        self.cleanup(local_cache)
        self.assertTrue(os.path.exists(local_cache))
        endpoint = uuid.uuid4()
        port = 1000
        s3 = S3Cache(local_cache, bucket_name, port=port,
                     is_secure=False, host=endpoint)
        s3.connect()

    def testBucketExists(self):
        create = False
        s3 = self.bucketFactory(create)
        # does the bucket exist?
        self.assertFalse(s3.bucket_exists())
        # delete non-existent bucket
        self.assertFalse(s3.remove_bucket())

    def testBucketCreateAndDelete(self):
        create = True
        s3 = self.bucketFactory(create)
        # does the bucket exist?
        self.assertTrue(s3.bucket_exists())
        # delete non-existent bucket
        self.assertTrue(s3.remove_bucket())

    def testBucketDeleteError(self):
        create = False
        s3 = self.bucketFactory(create)
        # does the bucket exist?
        self.assertFalse(s3.bucket_exists())
        # delete non-existant bucket
        s3.remove_bucket()

    @raises(S3CacheBucketNotExistError)
    def testReadWriteOnNonExistentBucket(self):
        create = False
        s3 = self.bucketFactory(create)
        # does the bucket exist?
        self.assertFalse(s3.bucket_exists())
        # Try some operations on a non-existent bucket
        object_name = "bucket-does-not-exist.txt"
        f = s3.open(object_name, "r")

    @raises(S3CacheIOError)
    def testReadNonExistentFile(self):
        s3 = self.bucketFactory()
        object_name = "file-does-not-exist.txt"
        f = s3.open(object_name, "r")

    def testFileCreateAndDelete(self):
        for caching in (True, False):
            s3 = self.bucketFactory()
            s3.set_caching(caching)
            object_name = "/foo/bar.txt"
            content = "content"
            # Create an object
            f = s3.open(object_name, "w")
            f.write(content)
            bytes_written = f.close()
            self.assertEqual(bytes_written, len(content))
            self.assertTrue(s3.object_exists(object_name))
            # then delete it
            self.assertTrue(s3.remove_object(object_name))
            self.assertFalse(s3.object_exists(object_name))
            # Create an object again
            f = s3.open(object_name, "w")
            f.write(content)
            bytes_written = f.close()
            self.assertEqual(bytes_written, len(content))
            self.assertTrue(s3.object_exists(object_name))
            # Revove using file handle
            self.assertTrue(f.remove())
            self.assertFalse(s3.object_exists(object_name))

    def testTwoHandlesToSameFile(self):
        for caching in (True, False):
            s3 = self.bucketFactory()
            object_name = "/foo/bar.txt"
            content = "content"
            # Create an object
            f1 = s3.open(object_name, "w")
            f1.write(content)
            bytes_written = f1.close()
            self.assertEqual(bytes_written, len(content))
            self.assertTrue(f1.exists())
            self.assertTrue(s3.object_exists(object_name))
            f2 = s3.open(object_name, "r")
            self.assertTrue(f2.exists())
            self.assertTrue(f2.remove())
            # now both handles will should that the file doesn't exist
            self.assertFalse(s3.object_exists(object_name))
            self.assertFalse(f1.exists())
            self.assertFalse(f2.exists())

    def testLocallyCached(self):
        s3 = self.bucketFactory()
        # Turn on caching
        s3.set_caching(True)
        object_name = "/foo/cached.txt"
        f = s3.open(object_name, "w")
        f.close()
        self.assertTrue(f.cached())
        self.assertTrue(f.remove_cached())
        self.assertFalse(f.cached())
        self.assertTrue(f.exists())
        self.assertTrue(f.remove())
        self.assertFalse(f.exists())
        self.assertFalse(f.cached())
        # Turn off caching
        s3.set_caching(False)
        object_name = "/foo/no-cache.txt"
        f = s3.open(object_name, "w")
        f.close()
        self.assertFalse(f.cached())
        self.assertTrue(f.remove_cached())
        self.assertFalse(f.cached())
        self.assertTrue(f.exists())
        # Read from S3, and the file has to be cached for reading
        f = s3.open(object_name, "r")
        self.assertTrue(f.cached())
        f.close()
        self.assertTrue(f.remove())
        self.assertFalse(f.exists())
        self.assertFalse(f.cached())

    def testCreateAndAppendToFile(self):
        for caching in (True, False):
            s3 = self.bucketFactory()
            # Toggle caching
            s3.set_caching(caching)
            object_name = "new-file.txt"
            content = "content"
            # write a file
            f = s3.open(object_name, "w")
            f.write(content)
            bytes_written = f.close()
            self.assertEqual(bytes_written, len(content))
            self.assertTrue(s3.object_exists(object_name))
            # now append to it
            f = s3.open(object_name, "a")
            f.write(content)
            bytes_written = f.close()
            self.assertEqual(bytes_written, len(content) * 2)
            self.assertTrue(s3.object_exists(object_name))

    def testOverWriteExistingFile(self):
        for caching in (True, False):
            s3 = self.bucketFactory()
            # Toggle caching
            s3.set_caching(caching)
            object_name = "new-file.txt"
            content = "content"
            # write a file
            f = s3.open(object_name, "w")
            f.write(content)
            bytes_written = f.close()
            self.assertEqual(bytes_written, len(content))
            self.assertTrue(s3.object_exists(object_name))
            f = s3.open(object_name, "r")
            line = f.readline()
            f.close()
            self.assertEqual(line, content)
            # now append to it
            alternative_content = "Mary had a little lamb"
            self.assertNotEqual(content, alternative_content)
            f = s3.open(object_name, "w")
            f.write(alternative_content)
            bytes_written = f.close()
            self.assertEqual(bytes_written, len(alternative_content))
            self.assertTrue(s3.object_exists(object_name))
            f = s3.open(object_name, "r")
            line = f.readline()
            f.close()
            self.assertEqual(line, alternative_content)

    def testCreateAndDownloadFile(self):
        # Write a file out file
        object_name = "myfile1.txt"
        content = "content"
        s3 = self.bucketFactory()
        s3.set_caching(True)
        f = s3.open(object_name, "w")
        f.write(content)
        bytes_written = f.close()
        self.assertEqual(bytes_written, len(content))
        self.assertTrue(s3.object_exists(object_name))
        # Now check it content directly
        local_cache = s3.local_cache()
        local_filename = os.path.join(local_cache, object_name)
        self.assertTrue(os.path.exists(local_filename))
        local_content = _read_file(local_filename)
        self.assertEqual(local_content, content)
        # Now manually remove the file from local cache
        os.unlink(local_filename)
        self.assertFalse(os.path.exists(local_filename))
        # Open the file to read and see that it is downloaded
        # from the bucket
        f = s3.open(object_name, "r")
        line = f.readline()
        self.assertEqual(line, content)
        # Remove file
        self.assertTrue(s3.remove_object(object_name))
        self.assertFalse(s3.object_exists(object_name))
