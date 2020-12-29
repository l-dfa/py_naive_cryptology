# :filename: tests/test_hill.py
# to use: "cd tests; python test_hill.py"


# import std libs
import os
import sys
import unittest


# import 3rd parties libs


# import project's libs
# we need to add the project directory to pythonpath to find project's module(s) in development PC without installing it
basedir, _ = os.path.split(os.path.abspath(os.path.dirname(__file__)).replace('\\', '/'))
sys.path.insert(1, basedir)              # ndx==1 because 0 is reserved for local directory
import source.nmatrix as nm              # NOW we find nmatrix module if we import it
import source.hill    as hill            # && hill.py

class HillTest(unittest.TestCase):
    def setUp(self):
        self.plaintext = "ACT"
        self.key = nm.NMatrix([[6,24,1],[13,16,10],[20,17,15]])
        self.ciphertext = "POH"
        
    def tearDown(self):
        pass
    
    def test_encrypt(self):
        ciphertext = hill.encrypt(self.plaintext, self.key)
        self.assertEqual(ciphertext, self.ciphertext)
        
    def test_decrypt(self):
        plaintext  = hill.decrypt(self.ciphertext, self.key)
        self.assertEqual(plaintext, self.plaintext)


if __name__ == '__main__':
    unittest.main()


