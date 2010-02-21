import os, sys
from base64 import b64encode,b64decode

#v_in = b64encode(os.urandom(80))
v_in = b'/l1Jy0B8Nv73SE0KxXAQzXe13BpSIrN0wdG7jUuydn1wfEi0CT0sxSikuT6UDCB10wBcHfR6OLVLRXZKcmHijxvtGLAC64dtV6w9RhZMvbav1+0m5oOUTv7fOfGUDEeYCyHS1y8zEJc5SxqE4CUPdKrQgBsd+NkuGi0uqV1iYexQR3zzsAQW85hDznAmfgo6iy52/DUdDSMuZFxx4wZ8KzEXCJrl6Xf6Y3wDF1SnoJBdZrzsb4iPVPPg0BMp9R/KxmpskIUgOFwCzgGUFYn9FXwYVIV7Qu6nMBzxkxJWjyaCobgpEiLNEvEYz2QUXo+ki8x6RmzKkqlDtK02vaoMsN1410UcOMSyGEPVJbZM6Rknw/wA59m5Va8S68BeJSwR/A7437ZLjUR2r51UXObTHYZPSkRoAFU2EwM2/p4l9QvRmw+NcmsBIa0ybwGHGKmUxLX5zieOwuaVTCTfBOuZWYxdAEBIwlS4LSJKqcDCeE5Rbok5kqRXA6annXsSzpWF'
#v_in = b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
#k = b64decode(v_in)

# k is the input data for randomness. make sure "k" has enough entropy for you.
k=""
"""if len(sys.argv)>=2:
    k = sys.argv[1]
else:
    k = os.urandom(2)

print repr(k)
"""
from pseudorandom.space import Random
import hashlib

lstRandom = {}
duplicates=set([])
nonused = dict(zip(list(range(256*256)),list(range(256*256))))

duplicates2=set([])
nonused2 = dict(zip(list(range(256*256)),list(range(256*256))))

duplicates3=set([])
nonused3 = dict(zip(list(range(256*256)),list(range(256*256))))

duplicates4=set([])
nonused4 = dict(zip(list(range(256*256)),list(range(256*256))))


h_primes = [257    ,263    ,269    ,271    ,277    ,281 
    ,283    ,293    ,307    ,311    ,313    ,317    ,331    ,337    ,347    ,349 
    ,353    ,359    ,367    ,373    ,379    ,383    ,389    ,397    ,401    ,409 
    ,419    ,421    ,431    ,433    ,439    ,443    ,449    ,457    ,461    ,463 
    ,467    ,479    ,487    ,491    ,499    ,503    ,509    ]
#random_space = Random(size=(1,1)) # 6*4 = 24 bytes per block.
#random_space.add_entropy("123456")
# MD5: 16 bytes (8 reps)
# SHA1: 20 btes (10 reps)
# SHA256: 32 bytes (16 reps)

repetitions = 64
sz = 2
dsp = [0,1]
each = (256*256)//100
for i in range(256*256):
    if i % each == 0:
        sys.stderr.write("%.0f%% " %  (float(i*100)/(256*256)))
        sys.stderr.flush()
    k = chr((i//256)%256) + chr(i%256) 
    #kb = [ chr((i*p+i//p)%256) for p in h_primes[:22] ]
    #bytes1 = "".join(kb)
    
    #bytes = os.urandom(sz*repetitions)

    """
    hash = hashlib.md5()
    bytes = ""
    while len(bytes)<2*sz:
        hash.update(k)
        bytes += hash.digest()
    """
    
    
    
    #"""
    random_space = Random(size=(6,1)) # 6*4 = 24 bytes per block.
    random_space.add_entropy("b"+k+"!"+k+"."+k+"*") # should pad the input data to match blocks (24 bytes )
    #random_space.randomize(iterations=1, factor = 1000) # Internally computes data, increasing entropy, throwing away the resulting bytes.
    bytes = random_space.get_bytes(sz*repetitions)
    #"""
    sys.stdout.write(bytes)
    """
    for i2 in range(repetitions):
        txt2 = ord(bytes[dsp[0]+i2*sz])*256 + ord(bytes[dsp[1]+i2*sz])% 256
        #txt2=txt2[:2]
        if txt2 not in lstRandom:
            lstRandom[txt2] = [i] 
        else:
            lstRandom[txt2].append(i)
        lrt = len(lstRandom[txt2])

        if lrt == repetitions-3 and txt2 in nonused4:
            del nonused4[txt2]
        elif lrt == repetitions-2 and txt2 in nonused3:
            del nonused3[txt2]
        elif lrt == repetitions-1 and txt2 in nonused2:
            del nonused2[txt2]
        elif lrt == repetitions and txt2 in nonused:
            del nonused[txt2]
        elif lrt == repetitions+1:
            duplicates|=set([txt2])
        elif lrt == repetitions+2:
            duplicates2|=set([txt2])
        elif lrt == repetitions+3:
            duplicates3|=set([txt2])
        elif lrt == repetitions+4:
            duplicates4|=set([txt2])
    """
    
"""    
duplen = [ len(lstRandom[d]) for d in duplicates ]
lens = [ len(lstRandom[k]) for k in lstRandom]
#for d in duplicates:   print d,lstRandom[d]
globallen = float(sum(lens)) / (256**2)
maxduplen = max(duplen)
avgduplen = float(sum(duplen)) / len(duplen)
avglens = float(sum(lens)) / len(lens)

print
print "duplic (1: %d, 2: %d, 3: %d, 4: %d)  \nunused (1: %d, 2: %d, 3: %d, 4: %d)" % (
    len(duplicates), len(duplicates2), len(duplicates3), len(duplicates4), 
    len(nonused), len(nonused2), len(nonused3), len(nonused4),
    )
print "max dup len: %.2f   global len: %.3f  extra len: %.6f, %.6f     " % (maxduplen, globallen,  avglens,avgduplen)
"""
    
#print nonused
#print(txt2)

"""txt1 = random_space.get_bytes(256) # will create (at least) 256bytes of raw data and will return *exactly* 256bytes.
print(repr(txt1))
txt2 = random_space.get_hexbytes(256) # will create (at least) 256bytes of raw data and will return *exactly* 256bytes in hex format.
print(txt2)"""

#for i in range(32):
#    txt2 = random_space.get_hexbytes(64) # will create (at least) 256bytes of raw data and will return *exactly* 256bytes in hex format.
#    print(txt2)

#for i in range(2048):
#    sys.stdout.write(random_space.get_bytes(512))

#sys.stderr.write("total written: %d random bytes.\n" %  random_space.c_bytes)
