# :filename: tests/test_modulus_aux.py
# to use: "cd tests; python test_modulus_aux.py"


# import std libs
import os
import sys
import unittest
import statistics as stat

# import 3rd parties libs

# import project's libs
# we need to add the project directory to pythonpath to find project's module(s) in development PC without installing it
basedir, _ = os.path.split(os.path.abspath(os.path.dirname(__file__)).replace('\\', '/'))
sys.path.insert(1, basedir)              # ndx==1 because 0 is reserved for local directory
import source.modulus_aux as ma          # NOW we find modulus_aux module if we import it


class ModulusAuxTests(unittest.TestCase):

    def test_lcg(self):
        rgen = ma.lcg()
        m = 0                # here we calculate the mean
        rounds = 200000      # num of random numbers to read
        nchannels = 20                            # num of channels to use to count how many numbers have a given magnitude
        s = {key: 0 for key in range(nchannels)}  # here the counts
        #breakpoint()
        for n in range(rounds):
            r = next(rgen)
            if n == 0: r0 = r               # we'll assert this one
            m += r                          # calculating mean numerator
            ndx = round(r * (nchannels-1))  # calculating the owning channel
            s[ndx] = s[ndx] + 1             # incrementing the owning channel
        m = m / rounds                      # the mean
        #print()
        #print(f'mean: {m}')
        #print(f'spectre: {s}')
        #print()
        self.assertEqual(r0, 12345 / (2 << 29))
        self.assertTrue(((0.5-0.01) < m) and (m < (0.5+0.01)))

    def test_equiv_list(self):
        result = ma.equiv_list(9, 3, 2)
        self.assertEqual(result, [-15, -6, 3, 12, 21])

    def test_naive_invmod(self):
        i = ma.naive_invmod(3,11)
        self.assertEqual(i, 4)
        i = ma.naive_invmod(-3,11)
        self.assertEqual(i, 7)
        #i = nm.inv_mod(6, 26)
        #self.assertEqual(i, 7)
        with self.assertRaises(ValueError):   # inverse of a wrong number
            max = 13
            for n in range(1,max+1):
                x = ma.naive_invmod(n,max)
    
    def test_invmod(self):
        x = ma.invmod(3, 11)
        self.assertEqual(x, 4)
        #x = nm.modinv(6, 26)
        #self.assertEqual(x, 7)
        with self.assertRaises(ValueError):   # inverse of a wrong number
            x = ma.invmod(13, 13)

if __name__ == '__main__':
    unittest.main()
