# :filename: tests/test_schoolbook_rsa.py
# to use: "cd tests; python test_schoolbook_rsa.py"

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
import source.schoolbook_rsa as srsa                 # NOW we find rsa module if we import it


class RSATests(unittest.TestCase):

    def test_keys(self):
        # from https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Example
        with self.assertRaises(ValueError):   # not prime number
            pub, pri = srsa.keys(p=4, q=7)
        with self.assertRaises(ValueError):   # not prime number
            pub, pri = srsa.keys(p=7, q=10)
        pub, pri = srsa.keys(p=61, q=53)
        self.assertEqual(pub, (3233, 7,))
        self.assertEqual(pri, (3233, 223,))
        y = srsa.encrypt(65, pub)
        x = srsa.decrypt(y, pri)
        self.assertEqual(x, 65)

    
    def test_encrypt(self):
        # from https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Example
        pub = (3233, 17)
        y = srsa.encrypt(65, pub)
        self.assertEqual(y, 2790)

    def test_decrypt(self):
        # from https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Example
        pri = (3233, 413)
        x = srsa.decrypt(2790, pri)
        self.assertEqual(x, 65)


if __name__ == '__main__':
    unittest.main()
