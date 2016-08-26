from s3cache import s3cache

s3cache.setVerbosity(True)
s3cache.setCaching(False)

f = s3cache.open("/abc/world.txt","w")
f.write("Hello")
f.close() 

f = s3cache.open("/abc/world.txt","a")
f.write(" World")
f.close() 

f2 = s3cache.open("/abc/world.txt","r") 
print f2.readline()
f2.close()

s3cache.remove("/abc/world.txt")
