#!/usr/bin/env python
from s3cache import s3cache

s3 = s3cache("/tmp", "t13d-misc")

s3.setVerbosity(True)
s3.setCaching(False)

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
