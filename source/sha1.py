# :filename: sha1.py hash computation using sha-1
# 
# note <<< is circular left shift
#      ft is a function depending on the stage; it's in F[t-1]
#      Kt is a constant depending on the stage. it's in K[t-1]
#
# general steps are:
#     - pad message as multiple of 512 bytes
#     - divide padded message in blocks (xi) of 512 bits
#     - init result H with H0
#     - for each block xi calculate Hi
#         - divide block in words of 32 bits (xi_j with j:0-15)
#         - using J:0-79 as round counter
#         - for 4 stages (t:1-4)
#             - for 20 rounds
#                 - calculate word wj with j:(J//t+J%20), where wj = xi_j if 0<=j<=15, else (wj-16 xor wj-14 xor wj-8 xor wj-3) <<< 1
#                 - calculate Hi at stage t with Hi-1, ft, Kt, wj(s) for the current stage
#         - Hi = add mod 2^32 five equal parts of Hi with the 5 parts of Hi-1
#            
# use: s = sha1(msg)
# where: s         int - the sha-1 code of message msg
#        msg       nbitarray - the message to compute: NBitArray(message_as_bytestring)


# import user libs
try:
    import nbitarray as nba
except:
    import source.nbitarray as nba

K = [
    0x5a827999,
    0x6ed9eba1,
    0x8f1bbcdc,
    0xca62c1d6,
]

F = [
    lambda b, c, d: (b & c) | (~b & d),
    lambda b, c, d: b ^ c ^ d,
    lambda b, c, d: (b & c) | (b & d) | (c & d),
    lambda b, c, d: b ^ c ^ d,
]

H0 = [
    nba.NBitArray([0x67, 0x45, 0x23, 0x01]),
    nba.NBitArray([0xef, 0xcd, 0xab, 0x89]),
    nba.NBitArray([0x98, 0xba, 0xdc, 0xfe]),
    nba.NBitArray([0x10, 0x32, 0x54, 0x76]),
    nba.NBitArray([0xc3, 0xd2, 0xe1, 0xf0]),
]


def sha1(msg):
    '''compute sha-1 of message
       
       params msg     nbitarray - messsage to hash
       
       return sha-1 hash of message as integer
    '''
    padded = msg.padding()                        # pad message as multiple of 512 bytes
    blocks = padded.break_to_list(el=512)         # divide padded message in blocks (xi) of 512 bits
    h = H0                                        # init result H with H0
    for block in blocks:                          # for each block xi calculate H
        h = hash_computation(block, h)
    result = h[0] + h[1] + h[2] + h[3] + h[4]     # result as nbitarray
    result =  result.to_int()                     # convet result to int
    return result


def hash_computation(block, h):
    '''compute hash of input block
    
       params 
         - block     nbitarray - block of text, len is 512 bits
         - h         tuple of 5 nbitarray - each of 32 bits
       
       return h: a tuple of 5 nbitarray instances (a, b, c, d , e,) each instance of 32 bits
    '''
    wj = msg_schedule(block)
    hi = h
    mod = 2 << 31                               # 2 ** 32
    for roundn in range(0, 80):
        stage = roundn // 20 + 1
        hi = round(hi, wj[roundn], stage)
    result = []
    for ndx in range(0, len(hi)):
        item  = h[ndx].to_int()
        iitem = hi[ndx].to_int()
        result.append( nba.NBitArray(nba.int_to_bit_list((item + iitem) % mod, length=32)) )
    return tuple(result)


def msg_schedule(block):
    '''computer a 32bit word for each round
    
       params block      nbitarray - (padded) text of 512 bits
    
       return a tuple with 80 elements, each element is an nbitarray of 32 bits: (w0, w1, ... w79,)
       
       note with xi = break of h in 32 bits words
            wj[i] = xi[i]    if 0<=i<=15
            wj[i] = (wj[i-16] xor wj[i-14] xor wj[i-8] xor wj[i-3]) <<< 1
    '''
    xi = block.break_to_list()
    wj = []
    for ndx in range(0, 80):
        if ndx < 16:
            wj.append(xi[ndx])
        else:
            w = (wj[ndx-16] ^ wj[ndx-14] ^ wj[ndx-8] ^ wj[ndx-3]).__lshift__(1, circular=True)
            wj.append(w)
    return tuple(wj)


def round(h, wj, t):
    '''hash computation core function
    
       params: 
         - h      tuple of 5 nbitarray instances - each instance of 32 bits
         - wj     nbitarray instances - 32 bits
         - t      int - number of stage (from 1 to 4)
               
       returns h: a tuple of 5 nbitarray instances (a, b, c. d. e,)
    '''
    if t < 1 or t > 4:
        raise ValueError('number of stage out of permitted range (i.e. 1 to 4)')
    sa = h[0].__lshift__(5, circular=True)        # shifted "a"
    sb = h[1].__lshift__(30, circular=True)       # shifted "b"
    a = h[0].to_int()
    b = h[1].to_int()
    c = h[2].to_int()
    d = h[3].to_int()
    e = h[4].to_int()
    wj = wj.to_int()
    sa = sa.to_int()
    sb = sb.to_int()
    f = F[t-1](b, c, d)
    mod = 2 << 31                            # 2**32
    result_a = nba.NBitArray(nba.int_to_bit_list((e + f + sa + wj + K[t-1]) % mod, length=32))
    result_b = nba.NBitArray(nba.int_to_bit_list(a, length=32))
    result_c = nba.NBitArray(nba.int_to_bit_list(sb, length=32))
    result_d = nba.NBitArray(nba.int_to_bit_list(c, length=32))
    result_e = nba.NBitArray(nba.int_to_bit_list(d, length=32))
    return (result_a, result_b, result_c, result_d, result_e,)
    

def main():
    msg = nba.NBitArray(b'The quick brown fox jumps over the lazy dog')           # message 
    expected = '2fd4e1c67a2d28fced849ee1bb76e7391b93eb12'
    s = sha1(msg)
    print(f'{s:0>40x}\n{expected}')                   # print as 40 hex digits
    pass


if __name__ == '__main__':
    main()