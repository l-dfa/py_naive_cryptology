# :filename: tests/test_sha1.py
# to use: "cd tests; python test_sha1.py"

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
import source.sha1 as sha1               # NOW we find sha1 module if we import it ...
import source.nbitarray as nba           # ... and nbitarray module


class SHA1Tests(unittest.TestCase):

    def test_F(self):
        b = 0x01
        c = 0x01
        d = 0x01
        self.assertEqual(sha1.F[0](b,c,d), 0x01)
        self.assertEqual(sha1.F[1](b,c,d), 0x01)
        self.assertEqual(sha1.F[2](b,c,d), 0x01)
        self.assertEqual(sha1.F[3](b,c,d), 0x01)
        c = 0x02
        self.assertEqual(sha1.F[0](b,c,d), 0x00)
        self.assertEqual(sha1.F[1](b,c,d), 0x02)
        self.assertEqual(sha1.F[2](b,c,d), 0x01)
        self.assertEqual(sha1.F[3](b,c,d), 0x02)
    
    def test_sha1(self):
        # message and expected are from wikipedia: https://en.wikipedia.org/wiki/SHA-1#Example_hashes
        msg = nba.NBitArray(b'The quick brown fox jumps over the lazy dog')
        expected = '2fd4e1c67a2d28fced849ee1bb76e7391b93eb12'
        s = sha1.sha1(msg)
        self.assertEqual(f'{s:0>40x}', expected)

    
    

    


if __name__ == '__main__':
    unittest.main()
