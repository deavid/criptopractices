import os
import sys

o = os.urandom(65536)

i = 0
for c in o:
    i+=1
    sys.stdout.write("%02x" % ord(c))
    if i%2 == 0:
	sys.stdout.write("\n")
    