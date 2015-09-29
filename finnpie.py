# Written for Python2

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
def lsb(data):
    binary = ''
    bite = 0
    pos = 0
    for index in range(len(data)):
        pos = index % 8
        bite += ((ord(data[index]) & 1) << pos)
        if pos == 7:
            binary += chr(bite)
            bite = 0
    if len(data) % 8 != 0:
        binary += chr(bite)
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
