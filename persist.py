#!/usr/bin/env python
from s3cache import S3Cache

s3 = S3Cache("/tmp", "t13d-misc")
s3.connect()
s3.create_bucket()
assert(s3.bucket_exists())

s3.set_verbosity(True)
s3.set_caching(True)

f = s3.open("/tmp/world.txt", "w")
f.write("Hello")
f.close()

f = s3.open("/tmp/world.txt", "a")
f.write(" World")
f.close()

f2 = s3.open("/tmp/world.txt", "r")
f2.close()

assert(s3.object_exists("/tmp/world.txt"))
s3.remove_object("/tmp/world.txt")
