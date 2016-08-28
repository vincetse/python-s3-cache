from nose.tools import *
from nose import with_setup
import unittest
import os
import shutil
import tempfile
import uuid
from s3cache import s3cache


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
        s3 = s3cache(local_cache, bucket_name, port=port,
                     is_secure=False, host=endpoint)
        print endpoint, port
        if create:
            s3.createBucket()
        return s3

    def testBucketExists(self):
        create = False
        s3 = self.bucketFactory(create)

        # does the bucket exist?
        self.assertFalse(s3.bucketExists())

    def testCreateAndDownloadFile(self):
        # Write a file out file
        object_name = "myfile1.txt"
        content = "content"
        s3 = self.bucketFactory()
        f = s3.open(object_name, "w")
        f.write(content)
        f.close()

        # Now check it content directly
        local_cache = s3.localCache()
        local_filename = os.path.join(local_cache, object_name)
        self.assertTrue(os.path.exists(local_filename))
        local_content = _read_file(local_filename)
        self.assertEqual(local_content, content)

        # Now manually remove the file from local cache
        os.unlink(local_filename)
        self.assertFalse(os.path.exists(local_filename))

        # Open the file to read and see that it is downloaded from the bucket
        f = s3.open(object_name, "r")
        line = f.readline()
        self.assertEquals(line, content)

    @raises(IOError)
    def testOpenNonExistentFile(self):
        object_name = "myfile1.txt"
        s3 = self.bucketFactory()
        f = s3.open(object_name, "r")
