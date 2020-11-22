# :filename: nbitarray.py         a naive buffer
#
# main methods:
#
#   import nbitarray as nba
#   
#   ba = nba.NBitArray(list_of_hex)    # create instance
#   bb = nba.NBitArray(list_of_bits)   # create instance
#   len(ba)                    # number of bits
#   ba[ndx]                    # bit at index ndx
#   ba[ndx] = bit_as_integer   # set bit at index ndx
#   ba == bb                   # eq operator
#   str(ba)                    # string of bits
#   ba + bb                    # concatenation operator
#   ba ^ bb                    # xor operator (ba and bb of the same length)
#   ba << n                    # left shift, note: ba.__lshift__(n, circular=True) does a circular left shift
#   ba >> n                    # right shift, note: ba.__rshift__(n, circular=True) does a circular right shift
#   ba.get_byte(bit_ndx|byte_ndx=)  # return one byte as integer from indicated position
#   ba.set_byte(x, bit_ndx|byte_ndx=, lenght=)  # set x as one byte at indicated position for the indicated length in bits
#   ba.permutate(permutation_table)  # return a permutated NBitArray obeying to the given permutation table. ...
#                                    #  ... permutation table is a list of integers where index indicate the position of the output bit ...
#                                    #  ... and value at the index is the position of the input bit.
#   ba.bit_list()              # return the bit array content as a list of integers with values 0|1
#   ba.hex()                   # return the bit array content as a string of hex numbers
#   ba.swap_lr()               # return an NBitArray with left and right halves inverted. len(ba) must be even

# import std libs
import sys
from numbers import Number


BYTE_SIZE = 8

# note: our array is LEFT TO RIGHT. index 0 is on the left edge
# so we need calculate an offset starting from BYTE_SIZE

def set_bit(v, index, x, ltr=True):
    """Set the index:th bit of v to 1 if x is truthy, else to 0, and return the new value
    
       params
         - v        int or byte - source to change
         - index    int - index of bit to set
         - x        int or bool - 0 | any other value means 1
         - ltr      bool - True, by default, means left to right indexing, otherwise id right to left
         
       return new value
       
       note. 
         - this is from unwind@https://stackoverflow.com/questions/12173774/how-to-modify-bits-in-an-integer#12174051
         - we use lefto to right only 8 bits on the rightmost part of an int
    """
    if ltr:
        offset = BYTE_SIZE - index -1
    else:
        offset = index
    mask = 1 << offset   # Compute mask, an integer with just bit 'index' set.
    v &= ~mask          # Clear the bit indicated by the mask (if x is False)
    if x:
        v |= mask         # If x was True, set the bit indicated by the mask.
    return v            # Return the result, we're done.

def get_bit(v, index, ltr=True):
    if ltr:
        offset = BYTE_SIZE - index -1
    else:
        offset = index
    mask = 1 << offset
    return (v & mask) >> offset

def test_bit(v, index, ltr=True):
    if ltr:
        offset = BYTE_SIZE - index -1
    else:
        offset = index
    mask = 1 << offset
    return (v & mask)

def is_bit_list(l):
    '''true if argument is a list with 0|1 only, otherwise false'''
    if isinstance(l, list):
        for ndx in range(0, len(l)):
            if l[ndx] == 0 or l[ndx] == 1:
                continue
            else:
                return False
    else:
        return False
    return True

def int_to_bit_list(v, length=None):
    '''from integer to list of bits
    
       params
         - v           int - value to convert
         - length      int - how many bits will be in list, filled on left by 0s
                             if None, bits len will be the minimum
       
       return a list of 0|1
    '''
    if length is None:
        fmt_str = '{:b}'
    else:
        fmt_str = '{:0>' + str(length) + 'b}'
    return [int(item) for item in list(fmt_str.format(v))]

    
class NBitArray(object):
    '''
         - nbits     int - num of valid bits in array
         - _ba       bytearray - physical container of bits
         
       note. this class isn't derived from bytearray because len(NBitArray)
             return n.of bits. These could be not aligned with bytes.
             this observation drops validity of methods of bytearray: in every
             case we will need overimpose new algorithms to methods. So we use
             bytearray merely as an holder of our bits
    '''

    @property
    def bytes_size(self):
        '''array lenght in bytes'''
        return len(self._ba)
    
    @property
    def elem_size(self):
        '''n.of bits in one element of array (i.e. one byte)'''
        return BYTE_SIZE

    def __init__(self, bits):
        '''create an NBitArray instance
        
           params
             - bits         list of 0|1 - bits hold by array, 
                            int - number of 0s bits to hold
                            others - passed to bytearray
        '''
        if is_bit_list(bits):
            self.length = len(bits)
            nbytes, overflow = divmod(self.length, self.elem_size)
            if overflow:
                nbytes += 1
            self._ba = bytearray(nbytes)
            for ndx in range(0, self.length):
                array_index, bit_position = divmod(ndx, self.elem_size)
                self._ba[array_index] = set_bit(self._ba[array_index], bit_position, bits[ndx])
        elif isinstance(bits, int):
            self.length = bits
            nbytes, overflow = divmod(self.length, self.elem_size)
            if overflow:
                nbytes += 1
            self._ba = bytearray(nbytes)
        else:
            self._ba = bytearray(bits)
            self.length = len(self._ba) * self.elem_size
    
    def __len__(self):
        return self.length
    
    def __eq__(self, other):
        return str(self) == str(other)
    
    def __setitem__(self, index, value):
        if index > self.length:
            raise IndexError
        array_index, bit_position = divmod(index, self.elem_size)
        self._ba[array_index] = set_bit(self._ba[array_index], bit_position, value)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return NBitArray([self[x] for x in range(*index.indices(len(self)))])
        if index >= self.length:
            raise IndexError
        array_index, bit_position = divmod(index, self.elem_size)
        return get_bit(self._ba[array_index], bit_position)
    
    def __str__(self, sep=None):
        result = []
        for ndx in range(0, len(self)):
            result.append(str(self[ndx]))
            if sep is not None and ndx+1 < len(self) and (ndx+1) % self.elem_size == 0:
                result.append(sep)
        return ''.join(result)
    
    def __repr__(self, sep=None):
        result = self.__str__(sep=sep)
        return '0b' + result
    
    def __add__(self, other):
        result = NBitArray(len(self)+len(other))
        target_ndx = 0
        for ndx in range(0, len(self)):
            result[target_ndx] = self[ndx]
            target_ndx += 1
        for ndx in range(0, len(other)):
            result[target_ndx] = other[ndx]
            target_ndx += 1
        return result
    
    def __xor__(self, other):
        if len(self) != len(other):
            raise ValueError('operands of different length')
        return NBitArray([self[ndx]^other[ndx] for ndx in range(0,len(self))])

    def __lshift__(self, num, circular=False):
        if type(num) != int:
            raise TypeError
        bl = self.bit_list()
        for n in range(0, num):
            abit = bl.pop(0)
            abit = abit if circular else 0
            bl.append(abit)
        return NBitArray(bl)

    def __rshift__(self, num):
        if type(num) != int:
            raise TypeError
        bl = self.bit_list()
        for n in range(0, num):
            bl.pop()
            bl.insert(0, 0)
        return NBitArray(bl)
    
    def get_byte(self, bit_ndx=None, byte_ndx=None):
        '''return byte starting at bit_ndx or byte_ndx'''
        if bit_ndx is None and byte_ndx is None:
            raise IndexError
        if bit_ndx is None:
            bit_ndx = byte_ndx * self.elem_size
        result = self[bit_ndx:(bit_ndx+self.elem_size)]
        return int(str(result), base=2)

    def set_byte(self, x, bit_ndx=None, byte_ndx=None, length=BYTE_SIZE):
        '''set self byte with value x starting at bit_ndx or byte_ndx
           
           params
             - x         int or list of bits - value to set
             - bit_ndx   int - index of start target bit
             - byte_ndx  int - index of start target byte
             - length     int - how many bits compose x, default is 8
             
           return None
           WARNING: if bits==None, x has the minimum extension and it sets position
                    in array starting from bit_ndx, with versus left to right
        '''
        if bit_ndx is None and byte_ndx is None:
            raise IndexError
        if is_bit_list(x):
            val_x = int(''.join(x), base=2)
            list_x = x
        else:
            val_x = x
            #fmt_str = '{:0>'+str(self.elem_size)+'b}'
            #list_x = [int(item) for item in list(fmt_str.format(x))]
            list_x = int_to_bit_list(x, length=length)
        if val_x < 0 or val_x >= (2**self.elem_size) :
            raise ValueError
        if bit_ndx is None:
            bit_ndx = byte_ndx * self.elem_size
        for source_ndx in range(0, len(list_x)):
            self[bit_ndx] = list_x[source_ndx]
            bit_ndx += 1
        
    def permutate(self, pt):
        '''permutate self bits values using the pt permutation table
        
           params pt      list of ints - ndx of list is the output bit to set,
                                         "pt[ndx]-1" is the input bit to get value
           return a new, permutated, NBitaArray
        '''
        target = NBitArray([0,] * len(pt))   # an NBitArray of all 0es
        for target_ndx in range(0, len(pt)):
            source_ndx = pt[target_ndx] - 1
            target[target_ndx] = self[source_ndx]
        return target

    def bit_list(self):
        return [self[ndx] for ndx in range(0, len(self))]
    
    def hex(self, asint=False):
        step = BYTE_SIZE
        tail_len = len(self) % step
        result = [self.get_byte(bit_ndx=ndx) for ndx in range(0,len(self),step) if (ndx+step)<=len(self)]
        if not asint:
            result = "".join([f'{item:0>2x}' for item in result])
        if tail_len != 0:
            if not asint:
                result = result + ':' + str(self[-tail_len:])
            else:
                result.append(self[-tail_len:].bit_list())
        return result
    
    def swap_lr(self):
        if len(self) % 2:
            raise TypeError
        left  = self[:len(self)//2]
        right = self[len(self)//2:]
        return right + left

def main():
    pass

if __name__ == '__main__':
    main()