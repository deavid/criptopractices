import os, sys
from base64 import b64encode,b64decode

def printobj(obj):
    sys.stderr.write(exportobj(obj))

def printobjlist(lst):
    """for obj in lst:
	printobj(obj)
	print "|",
    print """
    sys.stderr.write(exportlst(lst))
    sys.stderr.write("\n")

def exportlst(lst,char="\n"):
    return char.join([exportobj(obj) for obj in lst])

    
    
def exportobj(obj):
    return "%04x%03x%04x%03x%04x%03x" % (
	obj[0]%(16**4),
	obj[3]%(16**3),
	obj[1]%(16**4),
	obj[4]%(16**3),
	obj[2]%(16**4),
	obj[5]%(16**3),
	)

def exportobj2(obj):
    return "%.6f, %.6f, %.6f | %.6f, %.6f, %.6f" % (
        float(obj[0])/(16**4),
        float(obj[1])/(16**4),
        float(obj[2])/(16**4),
        float(obj[3])/(16**3),
        float(obj[4])/(16**3),
        float(obj[5])/(16**3),
        )

#print "test"
#v_in = b64encode(os.urandom(8*8*6))
v_in = b'/l0Jy0B8Nv73SE0KxXAQzXe13BpSIrN0wdG7jUuydn1wfEi0CT0sxSikuT6UDCB10wBcHfR6OLVLRXZKcmHijxvtGLAC64dtV6w9RhZMvbav1+0m5oOUTv7fOfGUDEeYCyHS1y8zEJc5SxqE4CUPdKrQgBsd+NkuGi0uqV1iYexQR3zzsAQW85hDznAmfgo6iy52/DUdDSMuZFxx4wZ8KzEXCJrl6Xf6Y3wDF1SnoJBdZrzsb4iPVPPg0BMp9R/KxmpskIUgOFwCzgGUFYn9FXwYVIV7Qu6nMBzxkxJWjyaCobgpEiLNEvEYz2QUXo+ki8x6RmzKkqlDtK02vaoMsN1410UcOMSyGEPVJbZM6Rknw/wA59m5Va8S68BeJSwR/A7437ZLjUR2r51UXObTHYZPSkRoAFU2EwM2/p4l9QvRmw+NcmsBIa0ybwGHGKmUxLX5zieOwuaVTCTfBOuZWYxdAEBIwlS4LSJKqcDCeE5Rbok5kqRXA6annXsSzpWF'
#v_in = b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
k = b64decode(v_in)
# 0.cuerpos * 1.variables * 2.precisionvars
# Min: 1*6*1 = 6 bytes (48bits)
#sz_sem = [1,6,1]
# Optimo: 6*6*3 = 108 bytes
#sz_sem = [6,6,3] 
# Grande: 20*6*2 = 240 bytes
#sz_sem = [20,6,2]
# Enorme: 60*6*4 = 1440 bytes
#sz_sem = [60,6,4]
sz_sem = [4,6,4]

k = k[:sz_sem[0]*sz_sem[1]*sz_sem[2]]
s = [] 
for i in range(sz_sem[0]):
    j=[]
    for n in range(sz_sem[1]): j.append(0)
    s.append(j)

for i,c in enumerate(k):
    n = i // sz_sem[2] // sz_sem[1]
    nt = (i - n*sz_sem[2]*sz_sem[1])//sz_sem[2]
    ntt = (i - n*sz_sem[2]*sz_sem[1] - nt*sz_sem[2])
    #print n,nt,ntt,ord(c)*(256**ntt)
    if type(c) is str: c = ord(c)
    m = len(k) / sz_sem[2]
    if sz_sem[2] >3: m = 1
    s[n][nt]+=(c-127)*(256**ntt)*m+i

s.append([209554,254220,234501,-5591,-7322,-472])
s.append([109554,-54220,334501,5591,7322,472])
sf = [ tuple(k) for k in s]
#print(s)
del s
#printobjlist(sf)
nums = []
newnum = 0
lastnum = 0
mybuffer = ""

#bytes_bloque = 2
#bloques = 2**(bytes_bloque*8)//2

bytes_bloque = 256//8
bloques = 2**4

total_bytes = bloques * bytes_bloque

#print total_bytes

xoraccums = {
}
primes = [2,3,5,7,11,13,17,19,23,29]
for p in primes:
    xoraccums[p] = list(range(p))
    
c_bytes = 0
g_bytes = 0
itera = 0
n_bi=0
for n in range(600000):
    if n%100 == 0: 
        sys.stderr.write("%d %d %.2f%%\n" % (n,c_bytes,100.0*c_bytes/total_bytes))
        
    if c_bytes > total_bytes: break
    
    for n1 in range(1):
        for i,k in enumerate(sf):
            for i2,j in enumerate(sf):
                if i==i2: continue
                kx, ky, kz, kfx, kfy, kfz = sf[i]
                jx, jy, jz, jfx, jfy, jfz = sf[i2]
                
                dx = (kx-jx)
                dy = (ky-jz)
                dz = (kz-jz)
                d = int(round(float(dx*dx+dy*dy+dz*dz)**(1/3.0)/1000.0) + 1)
                fx = dx // d
                fy = dy // d
                fz = dz // d
                jfx += fx
                jfy += fy
                jfz += fz
                jx+=jfx
                jy+=jfy
                jz+=jfz
                """jx-=jx/100
                jy-=jy/100
                jz-=jz/100"""
                j = jx, jy, jz, jfx, jfy, jfz 
                sf[i2]= j
                """
                kfx -= fx
                kfy -= fy
                kfz -= fz
                kx+=kfx
                ky+=kfy
                kz+=kfz
                k = kx, ky, kz, kfx, kfy, kfz 
                sf[i]= k
                """
    buf = exportlst(sf,"")
    g_bytes+=len(buf)/2
    if n>1:
        mybuffer+=buf
        #print(exportobj(sf[0]))
        while len(mybuffer)>5:
            newnum = int(mybuffer[:4],16)
            mybuffer = mybuffer[4:]
            kbits = int(mybuffer[:1],16)
            mybuffer = mybuffer[1:]
            desp_bits1 =  kbits % 4
            desp_bits2 =  (kbits//4) % 4
            desp_bits3 =  1
            #print "%08x" % newnum
            
            newnum2 = newnum & (2**desp_bits1-1)
            newnum >>= desp_bits1
            newnum |= newnum2 << (16-desp_bits1)
            
            lastnum2 = lastnum & (2**desp_bits2-1)
            lastnum >>= desp_bits2
            lastnum |= lastnum2 << (16-desp_bits2)
            itera += 1
            for k in xoraccums:
                i = xoraccums[k]
                m = itera % k
                xacc = i[m]
                xacc2 = xacc & (2**desp_bits3-1)
                xacc >>= desp_bits3
                xacc |= xacc2 << (16-desp_bits3)
                newnum ^= xacc
                i[m] = newnum
                
                

            newnum ^= lastnum
            lastnum = newnum
            if g_bytes>1024*5:
                nums.append((newnum & 255))
                nums.append(((newnum >> 8)& 255))
                c_bytes += 2
                #print "%04x" % newnum
        
        
        while len(nums)>0 and n_bi<total_bytes:
            num = nums.pop(0)
            n_bi+=1
            sys.stdout.write("%02x" % num)
            if n_bi%(bytes_bloque)==0: 
                sys.stdout.write("\n")
        
    #printobjlist(sf)

while len(nums)>0 and n_bi<total_bytes:
    num = nums.pop(0)
    n_bi+=1
    sys.stdout.write("%02x" % num)
    if n_bi%(bytes_bloque)==0: 
        sys.stdout.write("\n")

if n_bi%(bytes_bloque)!=0: 
    sys.stdout.write("-\n")
#print

#print xoraccums