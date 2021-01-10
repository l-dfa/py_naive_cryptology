# :filename: tests/test_nbitarray.py
# to use: "cd tests; python test_nbitarray.py"


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
import source.des       as des           # and des.py


# memo = {0x00: "0b_0000", 0x01: "0b_0001", 0x02: "0b_0010", 0x03: "0b_0011",
#         0x04: "0b_0100", 0x05: "0b_0101", 0x06: "0b_0110", 0x07: "0b_0111",
#         0x08: "0b_1000", 0x09: "0b_1001", 0x0a: "0b_1010", 0x0b: "0b_1011",
#         0x0c: "0b_1100", 0x0d: "0b_1101", 0x0e: "0b_1110", 0x0f: "0b_1111",
#        }

class OtherTests(unittest.TestCase):
    '''testing NBitArray module aux functions'''
    
    def test_set_bit(self):
        n = 0x00
        n = nba.set_bit(n, 0, 1)
        self.assertEqual(n, 0x80)
    
    def test_get_bit(self):
        n = 0x81
        n = nba.get_bit(n, 0)
        self.assertEqual(n, 0x01)
        n = nba.get_bit(n, 1)
        self.assertEqual(n, 0x00)

    def test_bit(self):
        n = 0x81
        n = nba.test_bit(n, 0)
        self.assertEqual(n, 0x80)
    
    def test_is_bit_list(self):
        bits = [0, 1, 1, 0]
        self.assertTrue(nba.is_bit_list(bits))
        nobits = [0, 2, 1, 0]
        self.assertFalse(nba.is_bit_list(nobits))

    def test_is_bit_string(self):
        bits = '0110'
        self.assertTrue(nba.is_bit_string(bits))
        nobits = '0210'
        self.assertFalse(nba.is_bit_list(nobits))
    
    def test_int_to_bit_list(self):
        l = nba.int_to_bit_list(10)
        self.assertEqual(l, [1,0,1,0,])
        l = nba.int_to_bit_list(10, length=8)
        self.assertEqual(l, [0,0,0,0,1,0,1,0,])
    
    def test_str_to_bit_list(self):
        l = nba.str_to_bit_list('10')
        self.assertEqual(l, [1,0,])


class NBitArrayTests(unittest.TestCase):
    '''testing NBitArray'''
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_elem_size(self):
        ba = nba.NBitArray([1,0,0,0,1,])
        self.assertEqual(ba.elem_size, 8)

    def test_bytes_size(self):
        ba = nba.NBitArray([1,0,0,0,1,])
        self.assertEqual(ba.bytes_size, 1)
    
    def test_init(self):
        ba = nba.NBitArray('011')
        self.assertEqual(len(ba), 3)   # these are 3 bits
        ba = nba.NBitArray([0,1,1,])
        self.assertEqual(len(ba), 3)   # these are 3 bits
        ba = nba.NBitArray(5)          # and these are 5
        self.assertEqual(len(ba), 5)
        ba = nba.NBitArray([0x00, 0x0a])    # 2 bytes: 16 bit
        self.assertEqual(len(ba), 2 * 8)
    
    def test_len(self):
        ba = nba.NBitArray([1,0,0,0,1,])
        self.assertEqual(len(ba), 5)
    
    def test_eq(self):
        ba0 = nba.NBitArray([1,0,0,0,1,])
        ba1 = nba.NBitArray([1,0,0,0,1,])
        self.assertEqual(ba0, ba1)
    
    def test_setitem(self):
        ba = nba.NBitArray([1,0,0,0,1,])
        ba[0] = 0
        ba[1] = 1
        i0 = ba[0]
        i1 = ba[1]
        self.assertEqual(i0, 0)
        self.assertEqual(i1, 1)
    
    def test_getitem(self):
        ba = nba.NBitArray([1,0,0,0,1,])
        i0 = ba[0]
        i1 = ba[1]
        self.assertEqual(i0, 1)
        self.assertEqual(i1, 0)
        i = ba[:2]
        self.assertTrue(isinstance(i, nba.NBitArray))
        self.assertEqual(str(i), '10')

    def test_str(self):
        ba = nba.NBitArray([0x81, 0x00])
        s = str(ba)
        self.assertEqual(s, '1000000100000000')
        s = ba.__str__(sep='_')
        self.assertEqual(s, '10000001_00000000')

    def test_repr(self):
        ba = nba.NBitArray([0x81, 0x00])
        s = ba.__repr__()
        self.assertEqual(s, '0b1000000100000000')
        s = ba.__repr__(sep='_')
        self.assertEqual(s, '0b10000001_00000000')

    def test_get_byte(self):
        ba = nba.NBitArray([0x81, 0x00])
        n0 = ba.get_byte(0)
        n1 = ba.get_byte(byte_ndx=1)
        self.assertEqual(n0, 0x81)
        self.assertEqual(n1, 0x00)
    
    def test_set_byte(self):
        ba = nba.NBitArray([0x81, 0x00])
        ba.set_byte(0x0a, byte_ndx=1)
        self.assertEqual(ba.get_byte(byte_ndx=1), 0x0a)
        ba.set_byte(0x0a, bit_ndx=4)
        self.assertEqual(ba.get_byte(bit_ndx=4), 0x0a)
        self.assertEqual(ba.get_byte(byte_ndx=1), 0xaa)
        ba = nba.NBitArray([0x81, 0x00])
        ba.set_byte(3, byte_ndx=1, length=None)
        self.assertEqual(ba.get_byte(byte_ndx=1), 0xc0)

    def test_permutate(self):
        ba = nba.NBitArray([0x80,0x80])
        pt = [16,  2,  3,  4,  5,  6,  7, 8,       # ba[15] => pba[0], ba[0] => pba[15]
               9, 10, 11, 12, 13, 14, 15, 1, ]
        pba = ba.permutate(pt)                     # pba: permutatd bit array
        self.assertEqual(str(pba[0:8]), '00000000')
        self.assertEqual(str(pba[8:16]), '10000001')

    def test_sum(self):
        ba = nba.NBitArray([0x01, 0x23])
        bb = nba.NBitArray([0x45, 0x67])
        bc = ba + bb
        self.assertEqual(len(bc), 4 * 8)
        self.assertEqual(bc.get_byte(byte_ndx=2), 0x45)
    
    def test_xor(self):
        ba = nba.NBitArray([0x0f, 0x0f])
        bb = nba.NBitArray([0x00, 0xff])
        bc = ba ^ bb                      # 0ff0
        self.assertEqual(bc.get_byte(byte_ndx=0), 0x0f)
        self.assertEqual(bc.get_byte(byte_ndx=1), 0xf0)
    
    def test_lshift(self):
        ba = nba.NBitArray([0x0f, 0x0f])
        bb = ba << 1
        self.assertEqual(bb.get_byte(byte_ndx=0), 0x1e)
        self.assertEqual(bb.get_byte(byte_ndx=1), 0x1e)
        ba = nba.NBitArray([0x8f, 0x0f])
        bb = ba.__lshift__(1, circular=True)
        self.assertEqual(bb.get_byte(byte_ndx=0), 0x1e)
        self.assertEqual(bb.get_byte(byte_ndx=1), 0x1f)

    def test_rshift(self):
        ba = nba.NBitArray([0x0f, 0x0f])
        bb = ba >> 1
        self.assertEqual(bb.get_byte(byte_ndx=0), 0x07)
        self.assertEqual(bb.get_byte(byte_ndx=1), 0x87)
        ba = nba.NBitArray([0x8f, 0x0f])
        bb = ba.__rshift__(1, circular=True)
        self.assertEqual(bb.get_byte(byte_ndx=0), 0xc7)
        self.assertEqual(bb.get_byte(byte_ndx=1), 0x87)

    def test_hex(self):
        ba = nba.NBitArray([0x0f,0xf0,])
        self.assertEqual(ba.hex(), '0ff0')
        ba = nba.NBitArray([0,0,0,0,1,1,1,1,1,1,1,1,])
        s = ba.hex()
        self.assertEqual(s, '0f:1111')
        ba = nba.NBitArray([0xff,])
        s = ba.hex(asint=True)
        self.assertEqual(s.pop(), 255)
        ba = nba.NBitArray([0xff,0xff])
        s = ba.hex()
        self.assertEqual(s, 'ffff')
        s = ba.hex(asint=True)
        self.assertEqual(s, [255, 255])
    
    def test_to_int(self):
        ba = nba.NBitArray([0xff,])
        self.assertEqual(ba.to_int(), 255)
        ba = nba.NBitArray([0xff, 0xff])
        self.assertEqual(ba.to_int(), 65535)
    
    def test_swap_lr(self):
        ba = nba.NBitArray([0x0f, 0xf0])
        swapped = ba.swap_lr()
        self.assertEqual(swapped.get_byte(byte_ndx=0), 0xf0)
        
    def test_padding(self):
        target = nba.NBitArray('01100001011000100110001110000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000011000')
        msg    = nba.NBitArray(b'abc')
        padded = msg.padding(md=128)
        self.assertEqual(padded, target)
        
    def test_break_to_list(self):
        ba = nba.NBitArray('1111000011110000')
        l = ba.break_to_list(el=4)
        self.assertEqual(len(l), 4)
        self.assertEqual(str(l[0]), '1111')

if __name__ == '__main__':
    unittest.main()


