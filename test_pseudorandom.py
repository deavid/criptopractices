import os, sys
from base64 import b64encode,b64decode

#v_in = b64encode(os.urandom(80))
v_in = b'/l1Jy0B8Nv73SE0KxXAQzXe13BpSIrN0wdG7jUuydn1wfEi0CT0sxSikuT6UDCB10wBcHfR6OLVLRXZKcmHijxvtGLAC64dtV6w9RhZMvbav1+0m5oOUTv7fOfGUDEeYCyHS1y8zEJc5SxqE4CUPdKrQgBsd+NkuGi0uqV1iYexQR3zzsAQW85hDznAmfgo6iy52/DUdDSMuZFxx4wZ8KzEXCJrl6Xf6Y3wDF1SnoJBdZrzsb4iPVPPg0BMp9R/KxmpskIUgOFwCzgGUFYn9FXwYVIV7Qu6nMBzxkxJWjyaCobgpEiLNEvEYz2QUXo+ki8x6RmzKkqlDtK02vaoMsN1410UcOMSyGEPVJbZM6Rknw/wA59m5Va8S68BeJSwR/A7437ZLjUR2r51UXObTHYZPSkRoAFU2EwM2/p4l9QvRmw+NcmsBIa0ybwGHGKmUxLX5zieOwuaVTCTfBOuZWYxdAEBIwlS4LSJKqcDCeE5Rbok5kqRXA6annXsSzpWF'
#v_in = b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
k = b64decode(v_in)

# k is the input data for randomness. make sure "k" has enough entropy for you.


from pseudorandom.space import Random

random_space = Random(size=(6,4)) # 6*4 = 24 bytes per block.
random_space.add_entropy(k[:64]) # should pad the input data to match blocks (24 bytes )
random_space.randomize(iterations=64) # Internally computes data, increasing entropy, throwing away the resulting bytes.

"""txt1 = random_space.get_bytes(256) # will create (at least) 256bytes of raw data and will return *exactly* 256bytes.
print(repr(txt1))
txt2 = random_space.get_hexbytes(256) # will create (at least) 256bytes of raw data and will return *exactly* 256bytes in hex format.
print(txt2)"""

for i in range(32):
    txt2 = random_space.get_hexbytes(64) # will create (at least) 256bytes of raw data and will return *exactly* 256bytes in hex format.
    print(txt2)

sys.stderr.write("total written: %d random bytes.\n" %  random_space.c_bytes)
