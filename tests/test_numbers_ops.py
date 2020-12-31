# :filename: tests/test_numbers_ops.py
# to use: "cd tests; python test_numbers_ops.py"

# import std libs
import os
import sys
import unittest
#import statistics as stat

# import 3rd parties libs

# import project's libs

# we need to add the project directory to pythonpath to find project's module(s) in development PC without installing it
basedir, _ = os.path.split(os.path.abspath(os.path.dirname(__file__)).replace('\\', '/'))
sys.path.insert(1, basedir)              # ndx==1 because 0 is reserved for local directory
import source.numbers_ops as nops          # NOW we find modulus_aux module if we import it


class NumbersOpsTests(unittest.TestCase):

    def test_egcd(self):
        # ax+by=gcd(a,b)
        g, x, y = nops.egcd(240, 46)
        #print(f"\ng: {g}, x: {x}, y: {y}")
        self.assertEqual(240*x+46*y, g)


    def test_coprimes(self):
        c = nops.coprimes(10)
        #print(f"\n{c}")
        self.assertEqual(len(c), 3)

    def test_coprimes_gen(self):
        gen = nops.coprimes_gen(10)
        self.assertEqual(type(gen), type((_ for n in range(5))))
        c = list(gen)
        #print(f"\n{c}")
        self.assertEqual(len(c), 3)

    def test_is_coprime(self):
        self.assertTrue(nops.is_coprime(4, 9))
        self.assertFalse(nops.is_coprime(4, 6))

    def test_is_prime_mr(self):
        self.assertTrue(nops.is_prime_mr(11))
        self.assertFalse(nops.is_prime_mr(10))

    def test_primes_gen(self):
        # http://www.primos.mat.br/indexen.html
        gen = nops.primes_gen(min=66)
        self.assertEqual(type(gen), type((_ for n in range(5))))
        self.assertEqual(len(list(gen)), 7)
        gen = nops.primes_gen(min=10000, max=10100)
        p = list(gen)
        #print(f"\n{p}, {len(p)}")
        self.assertEqual(len(p), 11)

    def test_primes(self):
        p = nops.primes(max=10)
        self.assertEqual(p, [2, 3, 5, 7, ])

    def test_lcm(self):
        # https://en.wikipedia.org/wiki/Least_common_multiple#Using_the_greatest_common_divisor
        self.assertEqual(nops.lcm(21, 6), 42)
        
    def test_is_prime(self):
        # http://www.primos.mat.br/indexen.html
        self.assertTrue(nops.is_prime(10007))
        self.assertFalse(nops.is_prime(10011))
        
    def test_gcd(self):
        self.assertEqual(nops.gcd(6, 35), 1)
        self.assertEqual(nops.gcd(1386, 3213), 63)
        
    def test_lcg(self):
        rgen = nops.lcg()
        m = 0                # here we calculate the mean
        rounds = 20000       # num of random numbers to read
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
        result = nops.equiv_list(9, 3, 2)
        self.assertEqual(result, [-15, -6, 3, 12, 21])

    def test_naive_invmod(self):
        i = nops.naive_invmod(3,11)
        self.assertEqual(i, 4)
        i = nops.naive_invmod(-3,11)
        self.assertEqual(i, 7)
        #i = nm.inv_mod(6, 26)
        #self.assertEqual(i, 7)
        with self.assertRaises(ValueError):   # inverse of a wrong number
            max = 13
            for n in range(1,max+1):
                x = nops.naive_invmod(n,max)
    
    def test_invmod(self):
        x = nops.invmod(3, 11)
        self.assertEqual(x, 4)
        #x = nm.modinv(6, 26)
        #self.assertEqual(x, 7)
        with self.assertRaises(ValueError):   # inverse of a wrong number
            x = nops.invmod(13, 13)

if __name__ == '__main__':
    unittest.main()
