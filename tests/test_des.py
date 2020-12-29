# :filename: tests/test_des.py
# to use: "cd tests; python test_des.py"


# import std libs
import os
import sys
import unittest


# import 3rd parties libs


# import project's libs
# we need to add the project directory to pythonpath to find project's module(s) in development PC without installing it
basedir, _ = os.path.split(os.path.abspath(os.path.dirname(__file__)).replace('\\', '/'))
sys.path.insert(1, basedir)              # ndx==1 because 0 is reserved for local directory
import source.nbitarray as nba           # NOW we find nbitarray module if we import it
import source.des       as des           # && des.py


class DesTests(unittest.TestCase):
    '''testing des.py'''

    def test_pbox(self):
        anin  = nba.NBitArray([0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, ])
        anout = nba.NBitArray([0x00, 0x00, 0x00, 0x80, 0x00, 0x00, 0x00, 0x02, ])
        a = des.pbox(anin, astype='start')
        self.assertEqual(a, anout)
        b = des.pbox(a, astype='stop')
        self.assertEqual(b, anin)
        #print()
        a = nba.NBitArray([0x12,0x34,0x56,0xab,0xcd,0x13,0x25,0x36,])
        t = nba.NBitArray([0x14,0xa7,0xd6,0x78,0x18,0xca,0x18,0xad,])
        a = des.pbox(a, astype='start', verbose=False)
        self.assertEqual(a, t)
        

    def test_permutate_using_expansion_box(self):
        # this is used in des_function
        # we test it because it is an expansion permutation; just to be sure ...
        #                 1               2                  3   
        #  1234   5678   9012   3456   7890   1234   5678   9012      ruler 4 bit
        #  0100   0100   0100   0100   0100   0100   0100   0100        source 4 bit
        #           1           2          3           4    
        # 123456 789012 345678 901234 567890 123456 789012 345678     ruler 6 bit
        # 001000 001000 001000 001000 001000 001000 001000 001000       target 6 bit
        # 0010 0000 1000 0010 0000 1000 0010 0000 1000 0010 0000 1000   target 4 bit
        # 0x20      0x82      0x08      0x20      0x82      0x08
        a = nba.NBitArray([0x44,0x44,0x44,0x44,])
        t = nba.NBitArray([0x20,0x82,0x08,0x20,0x82,0x08])
        b = a.permutate(des.EXPANSION_DBOX)
        self.assertEqual(b, t)
    
    def test_des_function(self):
        # round 1
        l0 = nba.NBitArray([0x14, 0xa7, 0xd6, 0x78,])
        r0 = nba.NBitArray([0x18, 0xca, 0x18, 0xad,])
        k1 = nba.NBitArray([0x19, 0x4c, 0xd0, 0x72, 0xde, 0x8c,])
        r1 = nba.NBitArray([0x5a, 0x78, 0xe3, 0x94,])
        #breakpoint()
        result = des.des_function(r0, k1)
        result = l0 ^ result
        self.assertEqual(result, r1)
        # 3rd round
        l2 = nba.NBitArray([0x5a,0x78,0xe3,0x94,])
        r2 = nba.NBitArray([0x4a,0x12,0x10,0xf6,])
        k3 = nba.NBitArray([0x06,0xed,0xa4,0xac, 0xf5, 0xb5,])
        r3 = nba.NBitArray([0xb8,0x08,0x95,0x91,])
        #breakpoint()
        result = des.des_function(r2, k3)
        result = l2 ^ result
        #print()
        #print(result.hex())
        #print(r3.hex())
        self.assertEqual(result, r3)
    
    def test_round_txt(self):
        txt0 = nba.NBitArray([0x14, 0xa7, 0xd6, 0x78, 0x18, 0xca, 0x18, 0xad,])
        the_key = des.Key([0xaa,0xbb,0x09,0x18,0x27,0x36,0xcc,0xdd,])
        # 1st round
        round = 1
        target = nba.NBitArray([0x18, 0xca, 0x18, 0xad, 0x5a, 0x78, 0xe3, 0x94,])
        result  = des.round_txt(txt0, the_key[round], round, verbose=False)
        self.assertEqual(result, target)
        # 2nd round
        round = 2
        target = nba.NBitArray([0x5a, 0x78, 0xe3, 0x94,0x4a,0x12,0x10,0xf6])
        result  = des.round_txt(result, the_key[round], round, verbose=False)
        self.assertEqual(result, target)
        # 3rd round
        round = 3
        target = nba.NBitArray([0x4a,0x12,0x10,0xf6,0xb8,0x08,0x95,0x91])
        result  = des.round_txt(result, the_key[round], round, verbose=False)
        self.assertEqual(result, target)

    def test_encrypt(self):
        #print()
        c = des.encrypt([0x12,0x34,0x56,0xab,0xcd,0x13,0x25,0x36,],
                        [0xaa,0xbb,0x09,0x18,0x27,0x36,0xcc,0xdd,],
                        verbose=False )                                # set this True to print intermediate results
        t = nba.NBitArray([0xc0,0xb7,0xa8,0xd0,0x5f,0x3a,0x82,0x9c,])
        self.assertEqual(c, t)

    def test_decrypt(self):
        #print()
        c = des.encrypt([0xc0,0xb7,0xa8,0xd0,0x5f,0x3a,0x82,0x9c,],
                        [0xaa,0xbb,0x09,0x18,0x27,0x36,0xcc,0xdd,],
                        reverse=True,
                        verbose=False )                                # set this True to print intermediate results
        t = nba.NBitArray([0x12,0x34,0x56,0xab,0xcd,0x13,0x25,0x36,])
        self.assertEqual(c, t)

class SBoxes(unittest.TestCase):

    def test_indices(self):
        # 1000 0001 1000 0001 1000 0001 1000 0001 1000 0001 1000 0001      bin x4; 48 total
        # 100000-011000-000110-000001-100000-011000-000110-000001          bin x6; 48 total
        # rccccr-rccccr-...
        a = nba.NBitArray([0x81, 0x81, 0x81, 0x81, 0x81, 0x81])
        r0, c0 = des.SBoxes._indices(1, a)
        r1, c1 = des.SBoxes._indices(2, a)
        self.assertEqual(r0, 2)
        self.assertEqual(c0, 0)
        self.assertEqual(r1, 0)
        self.assertEqual(c1, 0xc)
        #self.assertEqual(des.SBOXES[0][r0][c0], 4)

    def test_scrumble(self):
        ba = nba.NBitArray([1, 0, 0, 0, 1, 1,
                            0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0,
                            0, 0, 0, 0, 0, 0, ])
        target = nba.NBitArray([0xcf,0xa7,0x2c,0x4d,])
        bb = des.SBoxes.scrumble(ba)
        self.assertEqual(bb, target)
        ba = nba.NBitArray([1,0,0,1,0,1,       #3,2 -> 8
                            1,0,0,1,0,1,       #3,2 -> 10
                            1,0,1,0,1,0,       #2,5 -> 15
                            0,0,0,1,0,0,       #0,2 -> 14
                            0,1,1,1,1,1,       #1,f -> 6
                            0,1,1,1,0,0,       #0,e -> 5
                            1,0,1,1,1,1,       #3,7 -> 7
                            0,1,1,1,1,0, ])    #0,f -> 7
        #1000 1010 1111 1110 0110 0101 0111 0111 target
        target = nba.NBitArray([1,0,0,0, 1,0,1,0,
                                1,1,1,1, 1,1,1,0,
                                0,1,1,0, 0,1,0,1,
                                0,1,1,1, 0,1,1,1,] )
        bb = des.SBoxes.scrumble(ba)
        self.assertEqual(bb, target)

class KeyTests(unittest.TestCase):

    def test_key(self):
        data = [0xaa,0xbb,0x09,0x18,0x27,0x36,0xcc,0xdd,]
        k = des.Key(data)
        nbak = nba.NBitArray(data)
        self.assertEqual(k.key, nbak)

    def test_init(self):
        k = des.Key([0xaa,0xbb,0x09,0x18,0x27,0x36,0xcc,0xdd,])
        self.assertEqual(len(k._keys48), 16)

    def test_calculate_keys(self):
        k = des.Key([0xaa,0xbb,0x09,0x18,0x27,0x36,0xcc,0xdd,])
        k48_1  = nba.NBitArray([0x19,0x4c,0xd0,0x72,0xde,0x8c,])
        k48_16 = nba.NBitArray([0x18,0x1c,0x5d,0x75,0xc6,0x6d,])
        self.assertEqual(k[1], k48_1)
        self.assertEqual(k[16], k48_16)
        self.assertEqual(k[0], k.key_core)
    


if __name__ == '__main__':
    unittest.main()


