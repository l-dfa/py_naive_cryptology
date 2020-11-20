# :filename: des.py data encryption standard (DES) cipher
# 
# algorithm from Chapter_06_Data_Encription_Standard.pdf at https://academic.csuohio.edu/yuc/security/Chapter_06_Data_Encription_Standard.pdf
# and DES-NIST.FIPS.46-3.pdf at https://csrc.nist.gov/csrc/media/publications/fips/46/3/archive/1999-10-25/documents/fips46-3.pdf
#
# errata corridge of Chapter_06_Data_Encription_Standard.pdf:
#    where                       err        corr
#    p.147, table  6.2[7, 2]      31         30
#    p.148, table  6.3[1, 7]      10          1
#    p.148, table  6.3[1, 8]       3         10
#    p.149, table  6.8[3,12]      10          6
#    p.149, table 6.10[1,12]      10          0
#    p.149, table 6.10[2,11]      10         13
#    p.149, table 6.10[3,11]       9          0
#
# output of core function "encrypt" with reverse=False, verbose=True (see test_des.py)
# plaintext: 123456abcd132536
# key:       aabb09182736ccdd
# after start perm.: 14a7d67818ca18ad
# round   txt                     key48
# 1       18ca18ad 5a78e394       194cd072de8c
# 2       5a78e394 4a1210f6       4568581abcce
# 3       4a1210f6 b8089591       06eda4acf5b5
# 4       b8089591 236779c2       da2d032b6ee3
# 5       236779c2 a15a4b87       69a629fec913
# 6       a15a4b87 2e8f9c65       c1948e87475e
# 7       2e8f9c65 a9fc20a3       708ad2ddb3c0
# 8       a9fc20a3 308bee97       34f822f0c66d
# 9       308bee97 10af9d37       84bb4473dccc
# 10      10af9d37 6ca6cb20       02765708b5bf
# 11      6ca6cb20 ff3c485f       6d5560af7ca5
# 12      ff3c485f 22a5963b       c2c1e96a4bf3
# 13      22a5963b 387ccdaa       99c31397c91f
# 14      387ccdaa bd2dd2ab       251b8bc717d0
# 15      bd2dd2ab cf26b472       3330c5d9a36d
# 16      cf26b472 19ba9212       181c5d75c66d
# after straightening: 19ba9212cf26b472
# after stop perm.: c0b7a8d05f3a829c
#
# output of core function "encrypt" with reverse=True, verbose = True (i.e.: decrypt; see test_des.py)
# plaintext: c0b7a8d05f3a829c
# key:       aabb09182736ccdd
# after start perm.: 19ba9212cf26b472
# round   txt                     key48
# 1       cf26b472 bd2dd2ab       181c5d75c66d
# 2       bd2dd2ab 387ccdaa       3330c5d9a36d
# 3       387ccdaa 22a5963b       251b8bc717d0
# 4       22a5963b ff3c485f       99c31397c91f
# 5       ff3c485f 6ca6cb20       c2c1e96a4bf3
# 6       6ca6cb20 10af9d37       6d5560af7ca5
# 7       10af9d37 308bee97       02765708b5bf
# 8       308bee97 a9fc20a3       84bb4473dccc
# 9       a9fc20a3 2e8f9c65       34f822f0c66d
# 10      2e8f9c65 a15a4b87       708ad2ddb3c0
# 11      a15a4b87 236779c2       c1948e87475e
# 12      236779c2 b8089591       69a629fec913
# 13      b8089591 4a1210f6       da2d032b6ee3
# 14      4a1210f6 5a78e394       06eda4acf5b5
# 15      5a78e394 18ca18ad       4568581abcce
# 16      18ca18ad 14a7d678       194cd072de8c
# after straightening: 14a7d67818ca18ad
# after stop perm.: 123456abcd132536
#
# general algorithm of encrypt 
#
#         plaintext 64-bit                          cipher key 64(56)-bit                             plaintext 64-bit                
#               |                                            |                                               ^                         
#               v                                            |                                               |
#  initial permutation pbox(plain, start)                    |                             final permutation pbox(txt64, stop) 
#               |                                            |                                               |                         
#    round  1 round_txt(txt64, key48)  <----- k1  ---- round_key generator ----- k1  ---->  round 16 round_txt(txt64, key48) 
#               |                                            |                                               |                         
#    round  2 round_txt(txt64, key48)  <----- k2  -----------+----------- k2  ----------->  round 15 round_txt(txt64, key48) 
#              ...                                          ...                                             ...                        
#               |                                            |                                               |                         
#    round 16 round_txt(txt64, key48)  <----- k16 -----------+----------- k16 ----------->  round  1 round_txt(txt64, key48) 
#               |                                                                                            |
#  final permutation pbox(txt64, stop)                                                    initial permutation pbox(txt64, start)
#               |                                                                                            ^
#               v                                                                                            |
#         ciphertext 64-bit   -------------------------------------------------------------------------------+
#
# regarding algorithms about round_txt and round_key, see code or, better,
# the previously cited docs
#
# this module uses the auxiliary module nbitarray.py: a naive approach to array of bits


# import user libs
try:
    import nbitarray as nba
except:
    import source.nbitarray as nba

N_ROUNDS = 16

START_PT = [58, 50, 42, 34, 26, 18, 10,  2,     # initial permutation table
            60, 52, 44, 36, 28, 20, 12,  4,
            62, 54, 46, 38, 30, 22, 14,  6,
            64, 56, 48, 40, 32, 24, 16,  8,
            57, 49, 41, 33, 25, 17,  9,  1,
            59, 51, 43, 35, 27, 19, 11,  3, 
            61, 53, 45, 37, 29, 21, 13,  5,
            63, 55, 47, 39, 31, 23, 15,  7, ]
            
STOP_PT  = [40,  8, 48, 16, 56, 24, 64, 32,     # final permutation table
            39,  7, 47, 15, 55, 23, 63, 31,
            38,  6, 46, 14, 54, 22, 62, 30,
            37,  5, 45, 13, 53, 21, 61, 29,
            36,  4, 44, 12, 52, 20, 60, 28, 
            35,  3, 43, 11, 51, 19, 59, 27,
            34,  2, 42, 10, 50, 18, 58, 26,
            33,  1, 41,  9, 49, 17, 57, 25, ]
            
EXPANSION_DBOX = [32,  1,  2,  3,  4,  5,
                   4,  5,  6,  7,  8,  9,
                   8,  9, 10, 11, 12, 13, 
                  12, 13, 14, 15, 16, 17,
                  16, 17, 18, 19, 20, 21,
                  20, 21, 22, 23, 24, 25,
                  24, 25, 26, 27, 28, 29, 
                  28, 29, 30, 31, 32,  1, ]
                  
STRAIGHT_DBOX  = [16,  7, 20, 21, 29, 12, 28, 17,
                   1, 15, 23, 26,  5, 18, 31, 10,
                   2,  8, 24, 14, 32, 27,  3,  9,
                  19, 13, 30,  6, 22, 11,  4, 25, ]

#               0   1   2   3   4   5   6   7   8   9   a   b   c   d   e   f
SBOXES = [ [  [14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7,],               # start S-box 1
              [ 0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8,],
              [ 4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0,],
              [15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13,],  ],           # end   S-box 
              
           [  [15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10,],               # start S-box 2
              [ 3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5,],
              [ 0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15,],
              [13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9,],  ],           # end   S-box 
              
           [  [10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8,],
              [13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1,],
              [13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7,],
              [ 1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12,],  ],           # end   S-box 3
              
           [  [ 7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15,],
              [13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9,],
              [10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4,],
              [ 3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14,],  ],           # end   S-box 4
              
           [  [ 2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9,],
              [14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6,],
              [ 4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14,],
              [11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3,],  ],           # end   S-box 5
              
           [  [12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11,],
              [10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8,],
              [ 9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6,],
              [ 4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13,],  ],           # end   S-box 6
              
           [  [ 4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1,],
              [13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6,],
              [ 1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2,],
              [ 6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12,],  ],           # end   S-box 7
              
           [  [13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7,],
              [ 1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2,],
              [ 7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8,],
              [ 2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11,],  ],           # end   S-box 8
         ]                                                                                     # end   S-boxes

DROP_PARITY_BIT = [57, 49, 41, 33, 25, 17,  9,  1,
                   58, 50, 42, 34, 26, 18, 10,  2,
                   59, 51, 43, 35, 27, 19, 11,  3,
                   60, 52, 44, 36, 63, 55, 47, 39,
                   31, 23, 15,  7, 62, 54, 46, 38,
                   30, 22, 14,  6, 61, 53, 45, 37,
                   29, 21, 13,  5, 28, 20, 12,  4, ]

KEY_COMPRESSION = [14, 17, 11, 24,  1,  5,  3, 28,
                   15,  6, 21, 10, 23, 19, 12,  4,
                   26,  8, 16,  7, 27, 20, 13,  2,
                   41, 52, 31, 37, 47, 55, 30, 40,
                   51, 45, 33, 48, 44, 49, 39, 56,
                   34, 53, 46, 42, 50, 36, 29, 32, ]

class SBoxes(object):
    '''S-Boxes operation.
    
       note. we don't need to instantiate an S-Box.
             the only useful operation is the class
             method SBoxes.scrumble(txt48)
    '''
    _sboxes = SBOXES
    
    @classmethod
    def _indices(cls, snum, v):
        '''indices of s-box
        
           params
             - snum       int - number of s-box from 1 to 8, left to right
             - v          NBitArray - 48 bit integer to derive indices: 8 * 6 bits, 
                                each group of bits are rccccr where
                                rr are row index bits, cccc are column index bits
           return (row, col,) tuple to address s-box element
           
           note v is a 48 bit array. it is divided in 8 groups of 6 bits each.
                row is "1st, 6th" bits (left to right)
                col is "2nd, 3rd, 4th, 5th" bits 
                for each group
        '''
        if snum < 1 or snum > 8:
            raise IndexError
        if len(v) != 48:
            raise TypeError("value doesn't have 48 bits size")
        snum -= 1
        base = 6 * snum                        # 0, 1, ..42
        row_disps = (0, 5,)                   # row bits displacements: 1st, 6th
        col_disps = (1,2,3,4,)                # column bits displacements. 2nd, 3rd, 4th, 5th
        nrow = []
        ncol = []
        for ndx in range(0, len(row_disps)):
            abit = v[base + row_disps[ndx]]
            nrow.append(abit)
        for ndx in range(0, len(col_disps)):
            abit = v[base + col_disps[ndx]]
            ncol.append(abit)
        nrow = int( "".join([str(item) for item in nrow]), 2)
        ncol = int( "".join([str(item) for item in ncol]), 2)
        return (nrow, ncol,)
    
    @classmethod
    def scrumble(cls, v):
        '''text input to sboxes
        
           params
             - v         NBitArray - 48 bit text to scrumble
           
           return scrumbled text as NBitArray (32 bits)
        '''
        txt32 = nba.NBitArray([0,] * (4 * 8))  # 4*8 == 32 bits, all 0s
        step_size = 4                          # a nibble at time
        for num in range(1, 9):                # sbox number: 1 to 8, indices will be 0-7
            r, c = cls._indices(num, v)
            txt4 = cls._sboxes[num-1][r][c]
            txt32.set_byte(txt4, bit_ndx=(num-1)*step_size, length=step_size)
        return txt32

    
class Key(object):
    _one_key_shifting = { 1, 2, 9, 16, }   # these rounds (NOT indices) shift operands by one, the others by 2
    _drop_parity_bit = DROP_PARITY_BIT
    _key_compression = KEY_COMPRESSION

    @property
    def key(self):
        return self._key64
    
    @property
    def key_core(self):
        return self._key64.permutate(type(self)._drop_parity_bit)
    
    def __init__(self, key):
        self._key64  = nba.NBitArray(key)
        self._keys48 = self.calculate_keys()
        self._curr = -1
        
    def calculate_keys(self):
        '''calculate all 16 keys of 48 bits to use during rounds'''
        try:
            key56 = self.key_core     # drop parity bits and permutate
        except:
            raise ValueError('cannot calculate keys')
        result = []
        left  = key56[:len(key56)//2]
        right = key56[len(key56)//2:]
        for n in range(1, 17):          # rem.round is from 1 to 16 included
            if n in type(self)._one_key_shifting:
                left  = left.__lshift__(1, circular=True)
                right = right.__lshift__(1, circular=True)
            else:
                left  = left.__lshift__(2, circular=True)
                right = right.__lshift__(2, circular=True)
            tmp56 = left + right
            key48 = tmp56.permutate(type(self)._key_compression)
            result.append(key48)
        return result
    
    def __getitem__(self, num):
        '''get key at round num
           
           params
             - num     int - round to get
           
           return a 48 bit key as NBitArray 
                  if num == 0, return 56 bit initial key without parity bits
           
           note. num is from 1 to 16
        '''
        if num == 0:
            return self.key_core
        else:
            return self._keys48[num-1]
        
        
def encrypt(ptext, key, reverse=False, verbose=False):
    '''DES encryption/decryption
    
       params
         - ptext      list of hex - 64 bit plain text
         - key        list of hex - 64 bit == 56 bit cipher key + 8 parity bits
         - reverse    bool - if True, then decrypt; if False it encrypts
         - verbose    bool - if True prints intermediate results
       
       return ctext   NBitArray - 64 bit ciphertext
    '''
    nbptext = nba.NBitArray(ptext)            # nbptext: plain text as NBitArray instance
    k   = Key(key)                            # key as instance of Key
    if verbose:
        print('plaintext: {}'.format(nbptext.hex()))
        print('key:       {}'.format(k.key.hex()))
    if len(nbptext) != 64 or len(k.key) != 64:
        raise ValueError('wrong length of plaintext or key')
        
    txt = pbox(nbptext, astype='start', verbose=verbose)           # txt: working copy of NBitArray
    if verbose:
        print("round\ttxt\t\t\tkey48")
        
    for r in range(1, N_ROUNDS+1):                  # r is round number
        if reverse:
            kndx = N_ROUNDS + 1 - r
        else:
            kndx = r
        txt = round_txt(txt, k[kndx], r, verbose=verbose)
        
    # straightening last round
    txt = txt.swap_lr()
    if verbose:
        print('after straightening: {}'.format(txt.hex()))
        
    ctext = pbox(txt, astype='stop', verbose=verbose)              # ctext: ciphertext as NBitArray
    
    return ctext
    
def pbox(txt, astype='start', verbose=False):
    '''P-boxes
    
       params
         - txt            NBuffer instance - to elaborate
         - astype         str - start | stop:  initial or final permutation of bits
       return a permutated NBuffer instance
    '''
    if astype.lower() not in {'start', 'stop',}:
        raise ValueError(f'astype value "{astype}"is not acceptable')
    b = txt.permutate(START_PT) if astype=='start' else txt.permutate(STOP_PT)
    if verbose:
        print('after {} perm.: {}'.format(astype, b.hex()))
        #print('  as bin: {}'.format(b))
    return b
    
def round_txt(txt, key, round, verbose=False):
    '''
       params
         - txt         NBitArray - input text
         - key         NBitArray - cryptographic key
         
       returns an NBitArray
    '''
    if len(txt) != 64 or len(key) != 48:
        raise ValueError('wrong length of text or key, round {}'.format(round))
    left  = txt[:len(txt)//2]                  # left input
    right = txt[len(txt)//2:]                   # right input
    
    # mixer
    other_right = des_function(right, key)
    left = left ^ other_right
    
    # swapper: left part to right and viceversa
    result = right + left
    if verbose:
        print('{}\t{} {}\t{}'.format(round, right.hex(), left.hex(), key.hex()))

    return result

def des_function(txt, key):
    '''
       params
         - txt       NBitArray - input text
    '''
    txt48 = txt.permutate(EXPANSION_DBOX)       # expansion D-box
    
    txt48 = txt48 ^ key                         # XOR with key
    
    txt32 = SBoxes.scrumble(txt48)              # S-Boxes
    
    txt32 = txt32.permutate(STRAIGHT_DBOX)      # straight permutation
    return txt32

def main():
    plaintext = [0x12,0x34,0x56,0xab,0xcd,0x13,0x25,0x36,]
    cipherkey = [0xaa,0xbb,0x09,0x18,0x27,0x36,0xcc,0xdd,]
    bapt = nba.NBitArray(plaintext)
    back = nba.NBitArray(cipherkey)
    print(' encrypting hex text: {}'.format(bapt.hex()))
    print(' using hex key: {}'.format(back.hex()))
    c = encrypt(plaintext, cipherkey)
    print(' hex ciphertext is: {}'.format(c.hex()))
    print()
    print(' decrypting hex ciphertext: {}'.format(c.hex()))
    print(' using hex key: {}'.format(back.hex()))
    
    p = encrypt(c.hex(asint=True), cipherkey, reverse=True)
    print(' plain hex text is: {}'.format(p.hex()))
    
    

    def test_decrypt(self):
        #print()
        c = des.encrypt([0xc0,0xb7,0xa8,0xd0,0x5f,0x3a,0x82,0x9c,],
                        [0xaa,0xbb,0x09,0x18,0x27,0x36,0xcc,0xdd,],
                        reverse=True,
                        verbose=False )                                # set this True to print intermediate results
        t = nba.NBitArray([0x12,0x34,0x56,0xab,0xcd,0x13,0x25,0x36,])
        self.assertEqual(c, t)


if __name__ == '__main__':
    main()