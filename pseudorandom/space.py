import os, sys
from base64 import b64encode,b64decode

class SpaceObject:
    dim_for_size = {
        1 : 2,  
        2 : 2, 
        3 : 3,  #  px,py,pz = a[0],a[1],a[2] , fx,fy,fz = -a[1],-a[2],-a[0]
        4 : 3,  #  px,py,pz = a[0],a[1],a[2] , fx,fy,fz =  a[3],-a[2],-a[0]
        5 : 3,  #  px,py,pz = a[0],a[1],a[2] , fx,fy,fz =  a[3], a[4],-a[0]
        6 : 3,  #  px,py,pz = a[0],a[1],a[2] , fx,fy,fz =  a[3], a[4], a[5]
        
        7 : 4,  #  px,py,pz,pw = a[0],a[1],a[2],a[3] , fx,fy,fz,fw = -a[3], a[4], a[5], a[6]
        8 : 4,  #  px,py,pz,pw = a[0],a[1],a[2],a[3] , fx,fy,fz,fw =  a[4], a[5], a[6], a[7]
        
        9 :  6, 
        10 : 6, 
        11 : 6, 
        12 : 6, 
    }
    
    G = 0.00001
    def __init__(self,object, value_size):
        self.size = len(object)
        self.value_size = value_size # size of each number in bytes.
        assert(self.size in self.dim_for_size)
        self.dims = self.dim_for_size[self.size]
        self.position = []
        self.force = []
        self.entropy_position = value_size
        self.entropy_force = value_size 
        
        self.init_object(object)
        self.mass = sum(object)/len(object)/2**value_size
        if self.mass < 1 : self.mass = 1
    
    def get_state(self):
        pst = [ "%.6f" % (float(pos)/16**self.entropy_position) for pos in self.position ]
        frc = [ "%.6f" % (float(force)/16**self.entropy_force) for force in self.force ]
        return ", ".join(pst) + " | " + ", ".join(frc)
    
    def get_hex(self):
        mask1 = "%0" +("%d" % self.entropy_position)+"x"
        mask2 = "%0" +("%d" % self.entropy_force)+"x"
        
        pst = [ mask1 % (pos%16**self.entropy_position) for pos in self.position ]
        frc = [ mask2 % (force%16**self.entropy_force) for force in self.force ]
        final = [ "".join(z) for z in zip(pst,frc) ]
        return "".join(final)
    
        
        
    def init_object(self,a):
        p1 = p2 = p3 = p4 = p5 = p6 = 0
        f1 = f2 = f3 = f4 = f5 = f6 = 0
        if self.size == 1: p1 = a[0]; f2,f1 = -a[0],a[0]
        elif self.size == 2: p1,p2 = a[0],a[1]; f1,f2 = a[1],-a[0]
        elif self.size == 3: p1,p2,p3 = a[0],a[1],a[2]; f1,f2,f3 = -a[2],-a[1],a[1]
        elif self.size == 4: p1,p2,p3 = a[0],a[1],a[2]; f1,f2,f3 = -a[2],-a[1],a[3]
        elif self.size == 5: p1,p2,p3 = a[0],a[1],a[2]; f1,f2,f3 =  a[3], a[4],a[1]
        elif self.size == 6: p1,p2,p3 = a[0],a[1],a[2]; f1,f2,f3 =  a[3],-a[4],a[5]
        
        elif self.size == 7: p1,p2,p3,p4 = a[0],a[1],a[2],a[3]; f1,f2,f3,f4 =  a[3],-a[4],a[5],a[6]
        elif self.size == 8: p1,p2,p3,p4 = a[0],a[1],a[2],a[3]; f1,f2,f3,f4 =  a[4], a[5],a[6],a[7]
        
        elif self.size == 9: p1,p2,p3,p4,p5,p6 = a[0],a[1],a[2],a[3],a[4],a[5]; f1,f2,f3,f4,f5,f6 =  a[3],a[4],a[5],a[6],a[7],a[8]
        elif self.size == 10: p1,p2,p3,p4,p5,p6 = a[0],a[1],a[2],a[3],a[4],a[5]; f1,f2,f3,f4,f5,f6 =  a[4],a[5],a[6],a[7],a[8],a[9]
        elif self.size == 11: p1,p2,p3,p4,p5,p6 = a[0],a[1],a[2],a[3],a[4],a[5]; f1,f2,f3,f4,f5,f6 =  a[5],a[6],a[7],a[8],a[9],a[10]
        elif self.size == 12: p1,p2,p3,p4,p5,p6 = a[0],a[1],a[2],a[3],a[4],a[5]; f1,f2,f3,f4,f5,f6 =  a[6],a[7],a[8],a[9],a[10],a[11]

        if self.dims == 2:
            self.position = [p1,p2]
            self.force = [f1,f2]
        elif self.dims == 3:
            self.position = [p1,p2,p3]
            self.force = [f1,f2,f3]
        elif self.dims == 4:
            self.position = [p1,p2,p3,p4]
            self.force = [f1,f2,f3,f4]
        elif self.dims == 6:
            self.position = [p1,p2,p3,p4,p5,p6]
            self.force = [f1,f2,f3,f4,f5,f6]
        
        
    def advance_time(self,lstobjects, factor = 100):
        for obj in lstobjects:
            # calculate distance:
            distance = [(k-j) for k,j in zip(self.position,obj.position)]
            distance_2 = [ d**2 for d in distance]
            numeric_distance = sum(distance_2)**(1.0/float(self.dims))
            force = [ float(self.G * self.mass * obj.mass) / (d**2+1) for d in distance ]
            self.force = [ f1 + f2 for f1,f2 in zip(force,self.force) ]
            
        self.position = [ int(p + factor * f // self.mass) for p,f in zip(self.position,self.force)]
        
    
        


class Random:
    def __init__(self, size=(6,4)):
        self.num_variables = size[0]
        self.size_variables = size[1]
        self.padding = int(self.num_variables*self.size_variables)
        self.objects = []
        self.nums = []
        self.icycle = 0
        self.c_bytes = 0
        self.lastnum = 0
        self.xoraccums = {
        }
        self.primes = [
            2,3,
            5,7,
            #11,13,17,
            #19,23,29,
            ]
        self.buffer = ""
        for p in self.primes:
            self.xoraccums[p] = list(range(p))
        #v_in = b64decode(b'/l1Jy0B8Nv73SE0KxXAQzXe13BpSIrN0wdG7jUuydn1wfEi0CT0sxSikuT6UDCB10wBcHfR6OLVLRXZKcmHijxvtGLAC64dtV6w9RhZMvbav1+0m5oOUTv7fOfGUDEeYCyHS1y8zEJc5SxqE4CUPdKrQgBsd+NkuGi0uqV1iYexQR3zzsAQW85hDznAmfgo6iy52/DUdDSMuZFxx4wZ8KzEXCJrl6Xf6Y3wDF1SnoJBdZrzsb4iPVPPg0BMp9R/KxmpskIUgOFwCzgGUFYn9FXwYVIV7Qu6nMBzxkxJWjyaCobgpEiLNEvEYz2QUXo+ki8x6RmzKkqlDtK02vaoMsN1410UcOMSyGEPVJbZM6Rknw/wA59m5Va8S68BeJSwR/A7437ZLjUR2r51UXObTHYZPSkRoAFU2EwM2/p4l9QvRmw+NcmsBIa0ybwGHGKmUxLX5zieOwuaVTCTfBOuZWYxdAEBIwlS4LSJKqcDCeE5Rbok5kqRXA6annXsSzpWF')

        #self.add_entropy(v_in[:self.padding*3])


    def add_entropy(self,input_data):
        input_data = list(input_data)
        extra_input = len(input_data) % self.padding
        min_slices = 1
        pre_slices = len(input_data)//self.padding 
        konkatenar = list("era8324dsfgz9o845v3v26q5agzvzsdfsd425vb1745801475145be")
        if extra_input>0: extra_input = self.padding-extra_input
        if pre_slices < min_slices:
            extra_input+=self.padding*(min_slices-pre_slices)
        if extra_input>0:
            input_data = input_data + konkatenar[:extra_input]
        desp_bits3 = 1
        for i in range(3):
            for idx, c in enumerate(input_data):
                self.icycle += 1
                newnum = ord(c)
                for k in self.xoraccums:
                    i = self.xoraccums[k]
                    m = self.icycle % k
                    xacc = i[m]
                    xacc2 = xacc & (2**desp_bits3-1)
                    xacc >>= desp_bits3
                    xacc |= xacc2 << (8-desp_bits3)
                    newnum ^= xacc
                    self.xoraccums[k][m] = newnum
                    input_data[idx] = chr(newnum)

        slices = len(input_data)//self.padding
        #print slices, extra_input, len(input_data)
        for i in range(slices):
            space_object = input_data[i*self.padding:(i+1)*self.padding]
            self._add_entropy_object(space_object)
    
    def _add_entropy_object(self,space_object):
        assert(len(space_object) == self.padding)
        nvars = self.padding//self.size_variables
        assert(nvars == self.num_variables)
        final_object = []
        for i in range(nvars):
            binnumber = space_object[i*self.size_variables:(i+1)*self.size_variables]
            if len(binnumber) == 1:  binnumber = binnumber + binnumber
            number = self.from_bin_to_num(binnumber)
            final_object.append(number)
        sz = self.size_variables
        if sz < 2: sz = 2
        o = SpaceObject(final_object,sz)
        self.objects.append(o)
        #print(o.get_state())
            
            
    def from_bin_to_num(self,bin):
        n = 0
        for i,c in enumerate(bin):
            if type(c) is str: c = ord(c)
            n+=c*(256**i)
        n-= (256**len(bin))/2
        return n
        
    def compute(self,dryrun = False):
        mybuffer1 = self.buffer
        mybuffer = ""
        desp_bits3 =  1
        for ii in range(len(mybuffer1)//4):
            newnum = int(mybuffer1[ii*4:ii*4+4],16)
            
            
            for k in self.xoraccums:
                i = self.xoraccums[k]
                m = self.icycle % k
                xacc = i[m]
                xacc2 = xacc & (2**desp_bits3-1)
                xacc >>= desp_bits3
                xacc |= xacc2 << (16-desp_bits3)
                newnum ^= xacc
                self.xoraccums[k][m] = newnum
            mybuffer += "%04x" % abs(newnum & (2**16-1))
        #print "*", mybuffer1
        #print ">", mybuffer
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
            
            lastnum2 = self.lastnum & (2**desp_bits2-1)
            self.lastnum >>= desp_bits2
            self.lastnum |= lastnum2 << (16-desp_bits2)
            self.icycle += 1
            for k in self.xoraccums:
                i = self.xoraccums[k]
                m = self.icycle % k
                xacc = i[m]
                xacc2 = xacc & (2**desp_bits3-1)
                xacc >>= desp_bits3
                xacc |= xacc2 << (16-desp_bits3)
                newnum ^= xacc
                self.xoraccums[k][m] = newnum
                
                

            newnum ^= self.lastnum
            self.lastnum = newnum
            if not dryrun:
                self.nums.append((newnum & 255))
                self.nums.append(((newnum >> 8)& 255))
                self.c_bytes += 2
                #print "%04x" % newnum
        
        self.buffer = mybuffer
    
    def do_work(self,iterations1 = 1, iterations2 = 1, factor = 30, dryrun = False):
        assert(len(self.objects)>1) # It's impossible to compute random data with only ONE object. Should be at least 3.
        desp_bits3 = 1
        #print()
        for i in range(iterations1):
            for j in range(iterations2):
                for obj in self.objects:
                    obj.advance_time(self.objects,factor=factor)
                    for idx, val in enumerate(obj.position):
                        val = int(val)
                        for k in self.xoraccums:
                            i = self.xoraccums[k]
                            m = self.icycle % k
                            xacc = i[m]
                            val ^= xacc
                            obj.position[idx] += val & (2**8-1) - 127
                            
                    for idx, val in enumerate(obj.force):
                        val = int(val)
                        for k in self.xoraccums:
                            i = self.xoraccums[k]
                            m = self.icycle % k
                            xacc = i[m]
                            val ^= xacc
                            obj.force[idx] += val & (2**8-1) - 127
                            
                            
            lbuf = [obj.get_hex() for obj in self.objects]
            self.buffer = self.buffer + "".join(lbuf)
            self.compute(dryrun=dryrun)
    
    def randomize(self,iterations=32, factor = 1):
        self.do_work(iterations1=iterations, iterations2=1, factor = factor, dryrun = True)
        
    def get_bytes(self, nbytes):
        while len(self.nums)<nbytes: self.do_work()
        k = [ chr(n) for n in self.nums[:nbytes] ]
        self.nums=self.nums[nbytes:]
        return "".join(k)

    def get_hexbytes(self, nbytes):
        while len(self.nums)<nbytes: self.do_work()
        k = [ "%02x" % n for n in self.nums[:nbytes] ]
        self.nums=self.nums[nbytes:]
        return "".join(k)
        
            
    
        
        
        