# Written for Python2
from struct import Struct

# Performs XOR over two byte strings
# a and b do not have to be the same length
def xor(a,b):
    data = ''
    for index in range(len(a)):
        data += chr(ord(a[index]) ^ ord(b[index%len(b)]))
    return data

# constructs a byte string consisting of the least significant bit
# of the argument byte string
# resulting string length is ceil(len(data)/8.0)
# takes a Struct object to unpack the data
def lsb(data,struct=Struct('c'),msb=True):
    binary = ''
    bite = ''
    offset = 0
    while offset+struct.size<len(data):
        bite += str(struct.unpack_from(data,offset)[0] & 1)
        offset += struct.size
        if len(bite)==8:
            #print(bite)
            binary += chr(int(bite,2)) if msb else chr(int(bite[::-1],2))
            bite = ''
    if len(bite)>0:
        binary += chr(int(bite,2)) if msb else chr(int(bite[::-1],2))
    return binary

# returns the parity bit for a byte string
def parity(data):
    lookup = dict()
    for v in range(256):
        p = 0
        for bit in bin(v)[2:]:
            p ^= (1 if bit=='1' else 0)
        lookup[chr(v)] = p
    p = 0
    for x in data:
        p ^= lookup[x]
    return p

def brot(data,n):
    shiftarr = [128,192,224,240,248,252,254]
    result = ''
    n = n % 8
    if n==0:
        return data
    for x in data:
        result += chr((ord(x) >> n) | ((ord(x) << (8-n)) & shiftarr[n-1]))
    return result

def xshift(data, key, reverse=False):
    p = ''
    if reverse:
        data = data[::-1] + key
        for i in range(len(data)-1):
            p += xor(data[i],data[i+1])
        p = p[::-1]
    else:
        for i in range(len(data)):
            key = xor(data[i],key)
            p += key
    return p
