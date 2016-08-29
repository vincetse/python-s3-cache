import unittest
import tempfile
import shutil
from s3cache.utils import *


class TestUtils(unittest.TestCase):

    def setUp(self):
        self.cleanup_dirs = []

    def tearDown(self):
        for d in self.cleanup_dirs:
            shutil.rmtree(d)

    def cleanup(self, d):
        self.cleanup_dirs.append(d)

    def tempdir(self):
        temp = tempfile.mkdtemp()
        self.cleanup(temp)
        return temp

    def testMakedirs(self):
        temp = self.tempdir()

        makedirs(abspath(temp, "foo"))
        fullpath = os.path.join(temp, "foo")
        self.assertTrue(os.path.exists(temp))

        makedirs(abspath(temp, "/bar"))
        fullpath = os.path.join(temp, "bar")
        self.assertTrue(os.path.exists(temp))

        makedirs(abspath(temp, "magic/foo"))
        fullpath = os.path.join(temp, "magic")
        self.assertTrue(os.path.exists(temp))

        makedirs(abspath(temp, "/happy/camper"))
        fullpath = os.path.join(temp, "happy")
        self.assertTrue(os.path.exists(temp))

        makedirs(abspath(temp, "//happy1/camper"))
        fullpath = os.path.join(temp, "happy")
        self.assertTrue(os.path.exists(temp))

        makedirs(abspath(temp, "/happy2//camper"))
        fullpath = os.path.join(temp, "happy")
        self.assertTrue(os.path.exists(temp))

        makedirs(abspath(temp, "/happy3//foobar/camper"))
        fullpath = os.path.join(temp, "happy/foobar")
        self.assertTrue(os.path.exists(temp))
