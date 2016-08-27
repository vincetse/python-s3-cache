# S3 Cache for Python

[Niall McCarroll](http://www.mccarroll.net/) wrote a neat little [AWS S3 cache](http://www.mccarroll.net/snippets/s3boto/index.html) on his blog that I found really useful, but could not find on [PyPI](https://pypi.python.org/pypi), so here it is in a refactored form as a public service.

## Instructions

```
from s3cache import s3cache

s3 = s3cache("/tmp", BUCKET_NAME)

s3.setVerbosity(True)
s3.setCaching(False)

f = s3.open("/tmp/world.txt","w")
f.write("Hello")
f.close() 

f = s3.open("/tmp/world.txt","a")
f.write(" World")
f.close() 

f2 = s3.open("/tmp/world.txt","r") 
print f2.readline()
f2.close()

f3 = s3a.open("foobar.txt","w")
f3.write("Hello")
f3.close()

s3.remove("/tmp/world.txt")
```

## References

1. [A local file cache for amazon S3 using python and boto](http://www.mccarroll.net/snippets/s3boto/index.html)
