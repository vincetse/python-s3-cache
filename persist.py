#!/usr/bin/env python
from s3cache import S3Cache

s3 = S3Cache("/tmp", "t13d-misc")

s3.set_verbosity(True)
s3.set_caching(False)

f = s3.open("/tmp/world.txt", "w")
f.write("Hello")
f.close()

f = s3.open("/tmp/world.txt", "a")
f.write(" World")
f.close()

f2 = s3.open("/tmp/world.txt", "r")
print f2.readline()
f2.close()

s3.remove("/tmp/world.txt")
