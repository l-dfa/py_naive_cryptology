# :filename: tests/unit_tests.py
# to use: "cd tests; python unit_tests.py"


# import std libs
import os
import sys
import unittest

# import 3rd parties libs

class OtherTests(unittest.TestCase):

    def test_are_affine(self):
        self.assertTrue(nm.are_affine(3, 3))
        self.assertTrue(nm.are_affine(3, 3.0))
        self.assertTrue(nm.are_affine([3, 4], [3.0, 4.0]))
        self.assertFalse(nm.are_affine(2, [3.0, 4.0]))
        
    def test_naive_invmod(self):
        i = nm.naive_invmod(3,11)
        self.assertEqual(i, 4)
        i = nm.naive_invmod(-3,11)
        self.assertEqual(i, 7)
        #i = nm.inv_mod(6, 26)
        #self.assertEqual(i, 7)
        with self.assertRaises(ValueError):   # inverse of a wrong number
            max = 13
            for n in range(1,max+1):
                x = nm.naive_invmod(n,max)
    
    def test_invmod(self):
        x = nm.invmod(3, 11)
        self.assertEqual(x, 4)
        #x = nm.modinv(6, 26)
        #self.assertEqual(x, 7)
        with self.assertRaises(ValueError):   # inverse of a wrong number
            x = nm.invmod(13, 13)

class NMatrixTest(unittest.TestCase):
    '''testing NMAtrix'''
    
    def setUp(self):
        self.l = [ [ 0,  1,  2,  3,  4],
                   [10, 11, 12, 13, 14],
                   [20, 21, 22, 23, 24]  ]
        self.m = nm.NMatrix(self.l)
        
    def tearDown(self):
        pass
    
    def test_eq(self):
        A = nm.NMatrix([[1,2,3],[2,3,4]])
        B = nm.NMatrix([[1,2,3],[2,3,4]])
        self.assertTrue(A==B)
        B = nm.NMatrix([[1,2,3],[1,2,3]])
        self.assertFalse(A==B)
        
    def test_init(self):
        ''' NMatrix'''
        m = nm.NMatrix([ [0, 1, 2, 3],        # correct init
                      [10, 11, 12, 13]
                    ])
        self.assertEqual(m.shape, (2,4,))
        with self.assertRaises(ValueError):   # wrong init: 1st row has 5 elements, not 4
            m = nm.NMatrix([ [ 0,  1,  2,  3, 4],
                             [10, 11, 12, 13]   ])

    def test_getitem(self):
        self.assertEqual(self.m[0][0], 0)
        self.assertEqual(self.m[0], [0,1,2,3,4])
        self.assertEqual(self.m[0][0:3], [0,1,2])

    def test_setitem(self):
        m = nm.NMatrix([ [0, 1, 2], [10, 11, 12] ])
        m[0, 0] = 100
        self.assertEqual(m[0][0], 100)
        with self.assertRaises(ValueError):
            m[0,0] = [1, 2, 3]
        m[0] = [5, 6, 7]
        self.assertEqual(m[0][0], 5)

    def test_print(self):
        self.assertEqual(len(str(self.m)), len(str(self.l))+(len(self.l)-1))  # len of generating list + # of \n
    
    def test_getr(self):
        self.assertEqual(self.m.getr(0), self.l[0])
        with self.assertRaises(IndexError):   # wrong index; matrix has 3 rows, not 4
            self.m.getr(3)

    def test_getc(self):
        self.assertEqual(self.m.getc(0), [0,10,20])
        with self.assertRaises(IndexError):   # wrong index; matrix has 5 columns, not 6
            self.m.getc(5)

    def test_setc(self):
        A = nm.NMatrix([[1,2,3],[11,12,13],[21,22,23]])
        A.setc(1, [52, 62, 72])
        self.assertEqual(A[0,1], 52)
        self.assertEqual(A[1,1], 62)
        self.assertEqual(A[2,1], 72)

    def test_setr(self):
        A = nm.NMatrix([[1,2,3],[11,12,13],[21,22,23]])
        A.setr(1, [52, 62, 72])
        self.assertEqual(A[1], [52, 62, 72])

    def test_add(self):
        M1 = nm.NMatrix([[0, 0], [1, 1]])
        M2 = nm.NMatrix([[0, 0], [1, 1]])
        M3 = M1 + M2
        self.assertEqual(M3.getr(1), [2, 2])
        M3 = M1 + 2
        self.assertEqual(M3.getr(0), [2, 2])
        M1.__add__(M2, inplace=True)
        self.assertEqual(M1.getr(1), [2, 2])

    def test_sub(self):
        l2 = [ [ 0,  0,  0,  0,  0],
               [ 1,  1,  1,  1,  1],
               [ 2,  2,  2,  2,  2]  ]
        M2 = nm.NMatrix(l2)
        M3 = self.m - M2
        self.assertEqual(M3.getr(1), [9, 10, 11, 12, 13])
        M3 = M2 - 2
        self.assertEqual(M3.getr(1), [-1] * 5)
        M2.__sub__(2, inplace=True)
        self.assertEqual(M2.getr(1), [-1] * 5)

    def test_mul(self):
        l2 = [ [ 0,  0,  0],
               [ 0,  0,  0],
               [ 0,  0,  0],
               [ 0,  0,  0],
               [ 0,  0,  0]  ]
        M2 = nm.NMatrix(l2)
        M3 = self.m * M2
        self.assertEqual(M3.getr(1), [0,0,0])
        l2 = [ [ 1,  1,  1],
               [ 1,  1,  1],
               [ 1,  1,  1],
               [ 1,  1,  1],
               [ 1,  1,  1]  ]
        M2 = nm.NMatrix(l2)
        M3 = self.m * M2
        self.assertEqual(M3.getr(1), [60,60,60])
        M3 = M2 * 2
        self.assertEqual(M3.getr(1), [2] * 3)
        M2.__mul__(2, inplace=True)
        self.assertEqual(M2.getr(1), [2] * 3)

    def test_div(self):
        A = nm.NMatrix([[1,3,1],[3,2,5],[2,2,2]]) 
        B = A.inv()             # B == 1/A
        C = A / B               # A * (1/A) == A * A  -+
        C = round(C, 4)         #                      |
        D = A * A               #                      |
        self.assertEqual(D, C)  # <--------------------+

    def test_identity(self):
        E = nm.NMatrix.identity(3)
        self.assertTrue(sorted(E.as_list_of_lists()) == sorted([[1,0,0],[0,1,0],[0,0,1]]))

    def test_zeros(self):
        Zs = nm.NMatrix.zeros(3)
        self.assertTrue(sorted(Zs.as_list_of_lists()) == sorted([[0,0,0] for x in range(0,3)]))
        Zs = nm.NMatrix.zeros(3, 4)
        self.assertTrue(sorted(Zs.as_list_of_lists()) == sorted([[0,0,0,0]  for x in range(0,3)]))
    
    def test_randoms(self):
        Zs = nm.NMatrix.randoms(3, 3, range(-1, 10))
        #print(Zs)
        self.assertEqual(Zs.shape, (3,3,))
        Zs = nm.NMatrix.randoms(3)
        #print(Zs)
        self.assertEqual(Zs.shape, (3,3,))

    
    def test_inv_mod0(self):
        A = nm.NMatrix([[1,2],[3,4]])        # this is ok
        inv_A_m7 = A.inv_mod0(7)              # it must be [[5,1][5,3]]
        #breakpoint()
        self.assertTrue(sorted(inv_A_m7.as_list_of_lists()) == sorted([[5,1],[5,3]]))
        
        # from https://www.geeksforgeeks.org/hill-cipher/
        # [6,24,1|13,16,19|20,17,15]^-1 => [8,5,10|21,8,21|21,12,8](mod 26)
        A = nm.NMatrix([[6,24,1],[13,16,10],[20,17,15]]) 
        with self.assertRaises(ValueError):            # 1st col has all nums not invertable with mod 26
            inv_A_m26 = A.inv_mod0(26)
            #print(inv_A_m26)

    def test_inv_mod(self):
        A = nm.NMatrix([[1,2],[3,4]])        # this is ok
        inv_A_m7 = A.inv_mod(7)              # it must be [[5,1][5,3]]
        #breakpoint()
        self.assertTrue(sorted(inv_A_m7.as_list_of_lists()) == sorted([[5,1],[5,3]]))
        
        # from https://www.geeksforgeeks.org/hill-cipher/
        # [6,24,1|13,16,19|20,17,15]^-1 => [8,5,10|21,8,21|21,12,8](mod 26)
        A = nm.NMatrix([[6,24,1],[13,16,10],[20,17,15]]) 
        inv_A_m26 = A.inv_mod(26)
        #print(inv_A_m26)
        self.assertTrue(sorted(inv_A_m26.as_list_of_lists()) == sorted([[8,5,10],[21,8,21],[21,12,8]]))
    
    def test_inv(self):
        # j) of https://math-exercises.com/matrices/inverse-matrix
        A = nm.NMatrix([[1,3,1],[3,2,5],[2,2,2]]) 
        B = A.inv()
        A_1 = nm.NMatrix([[-6/8,-4/8,13/8],[4/8,0/8,-2/8],[2/8,4/8, -7/8]]) 
        #print(round(B, 4))
        #print(A_1)
        self.assertTrue( round(B, 4) == A_1)
        
    def test_minor(self):
        A = nm.NMatrix([[6,24,1],[13,16,10],[20,17,15]])
        A2 = A.minor(1, 2)
        self.assertEqual(len(A2), 2)
        self.assertEqual(A2[0], [6,  24])
        self.assertEqual(A2[1], [20, 17])

    def test_round(self):
        A = nm.NMatrix([[1.4, 2.6],[2.4, 3.6]])
        B = nm.NMatrix([[1, 3],[2, 4]])
        rA = round(A)
        self.assertTrue(rA==B)
        
    def test_s_mul(self):
        m = nm.NMatrix([[0,1,2],[10,11,12],[20,21,22]])
        m2 = m.s_mul(2)
        self.assertEqual(m2[0][1], 2)
        m = m.s_mul(2, inplace=True)
        self.assertEqual(m[0][1], 2)

    def test_s_add(self):
        m = nm.NMatrix([[0,1,2],[10,11,12],[20,21,22]])
        m2 = m.s_add(2)
        self.assertEqual(m2[0][0], 2)
        m = m.s_add(2, inplace=True)
        self.assertEqual(m[0][0], 2)

    def test_s_sub(self):
        m = nm.NMatrix([[0,1,2],[10,11,12],[20,21,22]])
        m2 = m.s_sub(2)
        self.assertEqual(m2[0][0], -2)
        m = m.s_sub(2, inplace=True)
        self.assertEqual(m[0][0], -2)

    def test_s_div(self):
        m = nm.NMatrix([[0,1,2],[10,11,12],[20,21,22]])
        m2 = m.s_div(2)
        self.assertEqual(m2[0][2], 1)
        m = m.s_div(2, inplace=True)
        self.assertEqual(m[0][2], 1)

    def test_s_mod(self):
        m = nm.NMatrix([[0,1,2],[10,11,12],[20,21,22]])
        m2 = m.s_mod(2)
        self.assertEqual(m2[0][1], 1)
        m = m.s_mod(2, inplace=True)
        self.assertEqual(m[0][1], 1)

    def test_swapr(self):
        m = nm.NMatrix([[0,1,2],[10,11,12],[20,21,22]])
        m2 = m.swapr(0,1)
        self.assertEqual(m2[0][0], 10)
        m.swapr(0,1, inplace=True)
        self.assertEqual(m[0][0], 10)
        with self.assertRaises(IndexError):
            m.swapr(0,3)

    def test_get_ndx_pivotr(self):
        A = nm.NMatrix([[0,1,2],[10,11,12],[20,21,22]])
        n = A.get_ndx_pivotr(0, 0)
        self.assertEqual(n, 2)
        A = nm.NMatrix([[30,31,32],[10,11,12],[20,21,22]])
        n = A.get_ndx_pivotr(1, 1, down=True)
        self.assertEqual(n, 2)
        A = nm.NMatrix([[6,24,1],[17,16,10],[20,17,15]])  # (mod 26)
        n = A.get_ndx_pivotr(0, 0, down=True, mod=26)
        self.assertEqual(n, 1)
        
    def test_pivotr(self):
        M = nm.NMatrix([[0,1,2],[10,11,12],[20,21,22]])
        M2 = M.pivotr(0, 0)
        self.assertEqual(M2[0,0], 20)
        M.pivotr(1,1, inplace=True)
        self.assertEqual(M[1,1], 21)
        with self.assertRaises(IndexError):
            M.pivotr(3,3)
        M = nm.NMatrix([[20,21,22],[0,1,2],[10,11,22]])
        M.pivotr(1,1, down=True, inplace=True)
        self.assertEqual(M[1,1], 11)

    def test_rdet(self):
        # test values from https://integratedmlai.com/find-the-determinant-of-a-matrix-with-pure-python-without-numpy-or-scipy/
        A = nm.NMatrix([[-2,2,-3],[-1,1,3],[2,0,-1]])
        self.assertEqual(A.rdet(), 18)
        A = nm.NMatrix([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]])
        self.assertEqual(A.rdet(), 0)
        A = nm.NMatrix([[1,2,3,4],[8,5,6,7],[9,12,10,11],[13,14,16,15]])
        self.assertEqual(A.rdet(), -348)
        A = nm.NMatrix([[1,2,3,4,1],[8,5,6,7,2],[9,12,10,11,3],[13,14,16,15,4],[10,8,6,4,2]])
        self.assertEqual(A.rdet(), -240)
        
    def test_det(self):
        # test values from https://integratedmlai.com/find-the-determinant-of-a-matrix-with-pure-python-without-numpy-or-scipy/
        A = nm.NMatrix([[-2,2,-3],[-1,1,3],[2,0,-1]])
        #d = A.det()
        #print(d)
        self.assertEqual(A.det(), 18)
        A = nm.NMatrix([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]])
        self.assertEqual(A.det(), 0)
        A = nm.NMatrix([[1,2,3,4],[8,5,6,7],[9,12,10,11],[13,14,16,15]])
        self.assertEqual(A.det(), -348)
        A = nm.NMatrix([[1,2,3,4,1],[8,5,6,7,2],[9,12,10,11,3],[13,14,16,15,4],[10,8,6,4,2]])
        self.assertEqual(A.det(), -240)

class HillTest(unittest.TestCase):
    def setUp(self):
        self.plaintext = "ACT"
        self.alphabet = { 'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4,
                          'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9,
                          'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14,
                          'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19,
                          'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25,
                        }
        self.key = nm.NMatrix([[6,24,1],[13,16,10],[20,17,15]])
        self.ciphertext = "POH"
        
    def tearDown(self):
        pass
    
    def test_encrypt(self):
        ciphertext = hill.encrypt(self.plaintext, self.key, self.alphabet)
        self.assertEqual(ciphertext, self.ciphertext)
        
    def test_decrypt(self):
        plaintext  = hill.decrypt(self.ciphertext, self.key, self.alphabet)
        self.assertEqual(plaintext, self.plaintext)


if __name__ == '__main__':
    # we need to add the project directory to pythonpath to find covid module in development PC without installing it
    basedir, _ = os.path.split(os.path.abspath(os.path.dirname(__file__)).replace('\\', '/'))
    sys.path.insert(1, basedir)              # ndx==1 because 0 is reserved for local directory
    import source.nmatrix as nm              # NOW we find nmatrix module if we import it
    import source.hill    as hill            # as abos, about hill.py
    unittest.main()


