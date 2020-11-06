# :filename: nmatrix.py     naive matrix
# ©2020 luciano de falco alfano
# under a CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/) license
# author disclaims any and all liability for any direct or indirect damages resulting
#   from errors of content or due to its use
# to use: 
#   - import nmatrix as nm
#   - m = nm.NMatrix([row1, row2, ...])    where rows are lists of numbers of the same lenght
#   - m = m1 + m2
#   - m = m1 - m2
#   - m = m1 * m2
#   - m = nm.NMatrix([e00, e01], [e10, e11], [e20,e21])
#         => m.shape==(3,2,), m.nrows==3, m.ncols==2
#         => m.getr(0)==[e00, e01], m[0]==[e00, e01], m[0,0]==e00, 
#                if "m[0]=[d00, d01]" => m[0]==[d00, d01]
#                if "m[0,0]=d00"      => m[0,0]==d00
#         => m.getc(0)==[e00, e10, e20]
#         => print(m)==[[e00, e01],
#                       [e10, e11],
#                       [e20,e21]]
#   - scalar operations: s_add, s_sub, s_mul, s_div, s_mod
# to do unit tests:
#   - venv\Scripts\Activate
#   - cd tests
#   - python unit_tests.py

# import std libs
import timeit as tm
import secrets


def naive_invmod(a, p): 
    '''modular multiplicative inverse of "a" (mod p), naive approach
       
       parameters
         - a            int - numer to inverse
         - p            int - modulus
       return mod.mult.inv. as int, if exists, else it raises ValueError
       note: derived from https://www.geeksforgeeks.org/multiplicative-inverse-under-modulo-m/
    '''
    a = a % p; 
    for x in range(1, p) : 
        if ((a * x) % p == 1) : 
            return x 
    raise ValueError(f"{a} doesn't have an inverse under modulo {p}")

def egcd(a, b):
    '''extended euclidean algorithm (extended greatest common divisor)
    
    params: a, b     int - 
    returns (g, x, y,)
    note. remember ax+by = gcd(a, b)
    '''
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def invmod(a, m):
    '''modular multiplicative inverse of "a" (mod m), using egcd
    
    parameters
      - a        int - number to invert
      - m        int - modulus
    return a^-1(mod m)        an int - if it exists
           raise valueError if it doesn't exist
    note. remember: a * x ≡ 1 (mod m); where x is the modular multiplicative inverse of a
    '''
    if a < 0:
        a = a % m
    g, x, y = egcd(a, m)
    if g != 1:
        raise ValueError(f"{a} doesn't have an inverse under modulo {m}")
    else:
        return x % m

def are_affine(item, value):
    '''test for numeric or lists'''
    numerics = (int, float, )
    if (  (isinstance(item, numerics) and isinstance(value, numerics))
       or (isinstance(item, list) and isinstance(value, list))         ):
        return True
    else:
        return False

class NMatrix(object):
    '''a naive matrix
    
       instance data:
         - __m__            list of lists - each row of the matrix is an inner list
         - shape            tuple of 2 int - (n.rows, ncols,)
    '''
    @classmethod
    def identity(cls, n):
        return cls([[int(x==y) for x in range(0,n)] for y in range(0,n)])

    @classmethod
    def zeros(cls, nrows, ncols=None):
        '''a matrix of zeroes
        
           params:
             - nrows        int - num of rows
             - ncols        int - num of cols; if None m will be equal to n
        '''
        if ncols is None:
            ncols = nrows
        return cls([[0 for x in range(0, ncols)] for y in range(0, nrows)])

    @classmethod
    def randoms(cls, nrows, ncols=None, rands=None):
        '''a matrix of zeroes
        
           params:
             - n        int - num of rows
             - m        int - num of cols; if None m will be equal to n
        '''
        if ncols is None:
            ncols = nrows
        if rands is None:
            max = nrows * ncols * 10
            rnd = len(str(max))
            rands = [round(item / max, rnd) for item in range(0, max)]
        return cls([[secrets.choice(rands) for x in range(0, ncols)] for x in range(0, nrows)])
    
    @property
    def nrows(self):
        return self.shape[0]

    @property
    def ncols(self):
        return self.shape[1]

    def __eq__(self, M):
        return self.__m__ == M._get_core()
    
    def __init__(self, lol):
        '''init matrix instance
           params:
               - lol  list of lists - [[row1], [row2], ...], each row of the same lenght
        '''
        lr = len(lol)
        lc = len(lol[0])
        for ndx in range(0, lr):
            if len(lol[ndx])!=lc:
                raise ValueError('rows are of different lenghts')
        self.__m__ = lol
        self.shape = (lr, lc,)
    
    def __getitem__(self, key):
        '''access by indices
          
           params key   int or tuple
           return requested element
           
           remark use:
             - M[i]          to get a row, i starts from 0
             - M[i, j]       to pick element at row i, col j
             - you can use M[i][j] too, but this isn't homogeneous with writing by indices
        '''
        if isinstance(key, tuple):
            x, y = key
            return self.__m__[x][y]
        else:
            return self.__m__.__getitem__(key)

    def __setitem__(self, key, value):
        '''write by indices
          
           params 
             - key   int or tuple
             - value list or number
           return None
           
           remark use:
             - M[i] = [row]         to write a row, i starts from 0
             - M[i, j] = number     to write a number at row i, col j
        '''
        item = self.__getitem__(key)
        if not are_affine(item, value):
            raise ValueError("new value isn't affine to the old one")
        if isinstance(key, tuple):
            x, y = key
            self.__m__[x][y] = value
        else:
            self.__m__[key] = value

    def __str__(self):
        '''string representing matrix'''
        if self.nrows==0 or self.ncols==0:
            raise ValueError('matrix without a dimension')
        result = '['
        for ndx in range(0, self.nrows):
            if ndx > 0: result += ' '
            result += str(self.__m__[ndx])
            if ndx < (self.nrows - 1): result += ',\n'
        result += ']'
        return result
    
    def __add__(self, nm, inplace=False):
        '''adding two matrices, if nm isn't a matrix it calls
           the operator on the scalar
        
           params 
             - nm          NMatrix - right operand
             - inplace     bool - if True return self else a new NMatriw will be made
             
           return self or a new  NMatrix
        '''
        if type(nm)!=NMatrix:
            return self.s_add(nm, inplace=inplace)
            
        if self.nrows!=nm.nrows or self.ncols!=nm.ncols:
            raise ValueError('dimensions do not match')
        if inplace:
            target = self
        else:
            target = self.copy()
        for ndx in range(0, target.nrows):
            target[ndx] = [x+y for x,y in zip(target.__m__[ndx], nm.getr(ndx))]
        return target
        
    def __sub__(self, nm, inplace=False):
        '''subtracting two matrices, if nm isn't a matrix it calls
           the operator on the scalar
        
           params 
             - nm          NMatrix - right operand
             - inplace     bool - if True return self else a new NMatriw will be made
             
           return self or a new  NMatrix
        '''
        if type(nm)!=NMatrix:
            return self.s_sub(nm, inplace=inplace)
        
        if self.nrows!=nm.nrows or self.ncols!=nm.ncols:
            raise ValueError('dimensions do not match')
        if inplace:
            target = self
        else:
            target = self.copy()
        for ndx in range(0, target.nrows):
            target[ndx] = [x-y for x,y in zip(target.__m__[ndx], nm.getr(ndx))]
        return target
        
    def __mul__(self, nm, inplace=False):
        '''multiplying two matrices, if nm isn't a matrix it calls
           the operator on the scalar
        
           param  nm     NMatrix - right operand
           return a new  NMatrix (inplace ever false)
        '''
        if type(nm)!=NMatrix:
            return self.s_mul(nm, inplace=inplace)

        if self.ncols!=nm.nrows:
            raise ValueError('dimensions do not match')
        if inplace:
            raise ValueError('cannot multiply in place two matrices')
            
        result = []
        nr_left = 0
        while nr_left<self.nrows:
            row = []
            nc_right = 0
            while nc_right<nm.ncols:
                tmp = [x*y for x, y in zip(self.__m__[nr_left], nm.getc(nc_right))]
                elem = sum(tmp)
                row.append(elem)
                nc_right += 1
            result.append(row)
            nr_left += 1
        return NMatrix(result)

    def __truediv__(self, M, inplace=False):
        '''dividing two matrices as self*M.inv(), if M isn't a matrix it calls
           the operator on the scalar
        
           param  M      NMatrix - right operand
           return a new  NMatrix (inplace ever false)
        '''
        if type(M)!=NMatrix:
            return self.s_div(M, inplace=inplace)

        if not self.is_square() or not M.is_square or self.nrows!=M.nrows:
            raise ValueError('dimensions do not match, or not square matrix')
        if inplace:
            raise ValueError('cannot divide in place two matrices')
        Minv = M.inv()
        return self * Minv

    def __len__(self):
        '''return nrows'''
        return self.shape[0]
    
    def _get_core(self):
        '''return the matrix core element'''
        return self.__m__
    
    def as_list_of_lists(self):
        '''return the matrix as a list of lists, each inner list is a row'''
        return self.__m__.copy()
    
    def copy(self):
        '''return a copy of the matrix'''
        return NMatrix(self.as_list_of_lists())

    def is_square(self):
        '''True if the matrix is square: nrows==ncols'''
        return self.nrows==self.ncols

    def det(self):
        '''matrix determinant using gauss elimination to get an upper triangle form
        
           note: derived from  https://integratedmlai.com/find-the-determinant-of-a-matrix-with-pure-python-without-numpy-or-scipy/
        '''
        if not self.is_square():
            raise ValueError('not a square matrix')
        # 1. initialize
        A = self.copy()
        n = len(self)
        sign = +1
        # 2. row ops on A to get in upper triangle form
        for fd in range(0, n):         # 2.1. fd stands for focus diagonal
            for i in range(fd + 1, n): # 2.2. only use rows below fd row
                if A[fd,fd] == 0:      # 2.3. if diagonal is zero, it could be a rounding problem ...
                    #raise ValueError('zero in diagonal')
                    A[fd,fd] = 1e-18   #      ... so we try to change it to ~zero
                crScaler = A[i,fd] / A[fd,fd] # 2.4. cr is "current row"
                                       # 2.5 "cr - crScaler * fdRow", applied to all elements in row
                A[i] = [A[i,j] - crScaler * A[fd,j] for j in range(0, n)]
        # 3. once A is in upper triangle form ...
        result = 1
        for i in range(0, n):
            # ... product of diagonals is determinant
            result *= A[i][i] 
        result *= sign 
        result = int(round(result)) if abs(int(round(result)) - result) <= 1.0e-10 else result
        return result
        
    def rdet(self, mul=1):
        '''recursive determinant by decomposition in smaller matrices
           params:
             - mul        numeric - multiplyer of the determinat of the smaller matrix; start with +1
           note: 
             - derived from https://stackoverflow.com/questions/47465356/how-to-find-determinant-of-matrix-using-python
             - this is a recursive method; not so good for big matrices, 
                    because is a bit slower than "det" and uses a lot of more memory,
                    but it deals better with 0s on diagonal compared to "det"
        '''
        l = len(self)
        if l == 1:
           return mul * self[0,0]
        else:
           sign = -1
           sum = 0
           for i in range(0, l):
               B = self.minor(0, i)                         # build the smaller matrix wout row 0 and col i
               sign *= -1
               sum += mul * B.rdet(sign * self[0,i])        # recursive call on smaller matrix B
           return sum        
    
    def minor(self, i, j):
        '''return a matrix as self, without row i and col j'''
        l     = len(self)
        A = NMatrix.zeros(l-1)
        row=0
        for ndx in range(0, l-1):
            if row==i:
              row += 1
            A[ndx] = [self[row,col] for col in range(0, l) if col!=j]
            row += 1
        return A
    
    def inv_mod0(self, q): 
        '''inverse modulus q
        
           params q       int - in python 3,  a long that is the modulus
           return the inverse modulus q of self as Nmatrix 
           note: 
             - this is a variant of Gauss-Jordan algorithm (as in self.inv())
                 got from https://stackoverflow.com/questions/4287721/easiest-way-to-perform-modular-matrix-inversion-with-python
             - this algorithm dosn't resolve [6,24,1|13,16,19|20,17,15]^-1 => [8,5,10|21,8,21|21,12,8](mod 26)
                 because col 0 [6,13,20] is formed all by numbers without inverse modulus 26
        '''
        if not self.is_square():
            raise ValueError('not a square matrix')
        l = len(self)
        A    = self.copy()
        Ainv = NMatrix.identity(l)
        for i in range(0, l):                                      # scan rows
            #print(A)
            factor = None
            #n = A.get_ndx_pivotr(i, i, down=True, mod=q)      # if an element in diagonal hasn't modulus, we try to move it
            #if n is not None:
            #    A.swapr(i, n, inplace=True)
            #    Ainv.swapr(i, n, inplace=True)
            a = A[i, i]
            try:
                factor = invmod(a, q)
            except ValueError:
                pass
            if factor is None:
                 raise ValueError("TODO: deal with this case")
            A[i]    = [item  * factor % q for item in A[i]]        # calculate i-th row
            Ainv[i] = [item  * factor % q for item in Ainv[i]]     # same as previous
            for j in range(0, l):                                  # again: scan rows except the current one (i-th)
                if (i != j):
                    factor = A[j,i]
                    # this is numpy: "A[j] = (A[j] - factor * A[i]) % q"; is the following correct?
                    A[j]    = [(A[j,col] - factor * A[i,col]) % q for col in range(0,l)]
                    Ainv[j] = [(Ainv[j,col] - factor * Ainv[i,col]) % q for col in range(0,l)]
        #print(Ainv)
        return NMatrix(Ainv)
    
    def inv_mod(self, q):
        '''module inverse of matrix, algorithm 2
        
           params q       int - in python 3,  a long that is the modulus
           return the inverse modulus q of self as Nmatrix 
           note.  this algorithm is stronger than "inv_mod0"; 
                  it can resolve  [6,24,1|13,16,19|20,17,15]^-1 => [8,5,10|21,8,21|21,12,8](mod 26)
        '''
        l   = len(self)
        adj = NMatrix.zeros(l)
        for i in range(0, l):
          for j in range(0, l):
            adj[i, j] = ((-1)**(i+j) * int(round(self.minor(j, i).det()))) % q
        result = adj.s_mul(invmod(int(round(self.det())), q)).s_mod(q)
        return result

    def inv(self):
        '''inverse using Gauss Jordan
        
           note: 
             - matrix must be squared;
             - algorithm from: https://www.codesansar.com/numerical-methods/matrix-inverse-using-gauss-jordan-method-pseudocode.htm
               but there is an error in point #6; "for j=n+1 to 2*n" must be "for j=1 to 2*n"
        '''
        if not self.is_square():
            raise ValueError('not a square matrix')
        # 1. build augmented identity matrix
        #    i.e. [[e00, e01]   => [[e00, e01, 1, 0]
        #          [e10, e11]]      [e10, e11, 0, 1]]
        n = len(self)
        aug = []
        for ndx in range(0, n):
            row = self.__m__[ndx][:]
            row.extend([0] * n)
            row[n+ndx] = 1
            aug.append(row)
        # 2. Apply Gauss Jordan Elimination on Augmented Matrix
        for ndxr in range(0, n):
            if not aug[ndxr][ndxr]:
                raise ValueError('zero on diagonal; ndx: {}, aug: {}'.format(ndxr, aug[ndxr]))
            for ndxc in range(0, n):
                if ndxr!=ndxc:
                    ratio = aug[ndxc][ndxr] / aug[ndxr][ndxr]
                    for k in range(0, 2*n):
                        aug[ndxc][k] -= ratio * aug[ndxr][k]
        # 3. Row Operation to Convert Principal Diagonal to 1.
        for ndxr in range(0, n):
            divisor = aug[ndxr][ndxr]
            for ndxc in range( 2*n):
                aug[ndxr][ndxc] /= divisor
        # 4. get inverse
        result = []
        for row in aug:
            result.append(row[n : 2*n])
        return NMatrix(result)
        
    def swapr(self, n1, n2, inplace=False):
        '''swap two rows'''
        if inplace:
            target = self
        else:
            target = self.copy()
        tmp = target[n1].copy()
        target[n1] = target[n2]
        target[n2] = tmp
        return target

    def get_ndx_pivotr(self, i, j, down=False, mod=None):
        '''get pivot indices on the rows at [i,j] position
        
           params
             - i, j      int - indices(row, col) of element to pivot
             - down      bool - if true only rows with index>=i are permitted
             - mod       int - if None search for max, otherwise search for modulus existence
           
           return 
             - n         int -  index of row to swap with i
             - None      if swap isn't possible
        '''
        l = len(self)
        taboo = set()
        if down: taboo = taboo | set(list(range(0,i)))    # union
        
        col = {ndx: self.getc(j)[ndx] for ndx in range(0, l) if ndx not in taboo}
        themax = None
        ndxmax = None
        if mod is None:
            themax = max(col.values())
            ndxmax = max(col)
        else:
            for key, val in col.items():
                m = 0
                try:
                    m = invmod(val, mod)
                    themax = val
                    ndxmax = key
                except ValueError:
                    continue
        if themax is None or themax <= self[i,j]:
            return None
        else:
            return ndxmax
        
    def pivotr(self, i, j, down=False, mod=None, inplace=False):
        '''apply pivot on the rows at [i,j] position'''
        n = self.get_ndx_pivotr(i, j, down=down, mod=mod)
        if n is None:
            return self
        if inplace:
            target = self
        else:
            target = self.copy()
        target.swapr(i, n, inplace=True)
        return target

    def __round__(self, ndigits=None, inplace=False):
        if inplace:
            target = self
        else:
            target = self.copy()
        for ndx in range(0, target.nrows):
            target[ndx] = [round(item, ndigits=ndigits) for item in target[ndx]]
        return target
        
        
    def s_mul(self, n, inplace=False):
        '''scalar multiply by number
           
           params
             - n         number - the multiplier
             - inplace   bool - if True it modify self, otherwise a new matrix will be created
           
           return self or a new NMatrix
             '''
        if inplace:
            target = self
        else:
            target = self.copy()
        for ndx in range(0, target.nrows):
            target[ndx] = [el * n for el in target[ndx]]
        return target

    def s_add(self, n, inplace=False):
        '''scalar sum by number'''
        if inplace:
            target = self
        else:
            target = self.copy()
        for ndx in range(0, target.nrows):
            target[ndx] = [el + n for el in target[ndx]]
        return target

    def s_sub(self, n, inplace=False):
        '''scalar subtraction by number'''
        if inplace:
            target = self
        else:
            target = self.copy()
        for ndx in range(0, target.nrows):
            target[ndx] = [el - n for el in target[ndx]]
        return target

    def s_div(self, n, inplace=False):
        '''scalar division by number'''
        if inplace:
            target = self
        else:
            target = self.copy()
        for ndx in range(0, target.nrows):
            target[ndx] = [el / n for el in target[ndx]]
        return target

    def s_floordiv(self, n, inplace=False):
        '''scalar floor division by number'''
        if inplace:
            target = self
        else:
            target = self.copy()
        for ndx in range(0, target.nrows):
            target[ndx] = [el // n for el in target[ndx]]
        return target

    def s_mod(self, n, inplace=False):
        '''scalar modulus by number'''
        if inplace:
            target = self
        else:
            target = self.copy()
        for ndx in range(0, target.nrows):
            target[ndx] = [el % n for el in target[ndx]]
        return target

    def t(self):
        '''mtrix transpose'''
        result = []
        ndx = 0
        while ndx<self.shape[1]:
            result.append(self.getc(ndx))
            ndx += 1
        return NMatrix(result)

    def getr(self, ndx):
        '''get row by index'''
        #if ndx>=self.nrows:
        #    raise IndexError('index out of matrix dimension')
        return self[ndx]

    def getc(self, ndx):
        '''get column by index'''
        if ndx >= self.ncols:
            raise IndexError('index out of matrix dimension')
        column = [row[ndx] for row in self.__m__]
        return column

    def setr(self, nrow, lnums):
        '''set row by index'''
        self[nrow] = lnums

    def setc(self, ncol, lnums):
        '''set column by index'''
        if ncol >= self.ncols:
            raise IndexError('index out of matrix dimension')
        for nrow in range(0, self.nrows):
            self[nrow, ncol] = lnums[nrow]


def main():

    #import timeit as tm
    #print(tm.timeit("A.det_gj()", "import nmatrix as nm; A = nm.NMatrix([[-2,2,-3],[-1,1,3],[2,0,-1]])", number=100000))
    #print(tm.timeit("A.det()",    "import nmatrix as nm; A = nm.NMatrix([[-2,2,-3],[-1,1,3],[2,0,-1]])", number=100000))
    
    #A = NMatrix([[0,1],[1,1]]) # this is ok
    #inv_A_mod5 = A.inv_mod(5)  # it must be [[5,1][5,3]]
    #print(inv_A_mod5)
    
    ## https://www.geeksforgeeks.org/hill-cipher/
    ## https://www.khanacademy.org/computing/computer-science/cryptography/modarithmetic/a/modular-inverses
    #A = NMatrix([[6,24,1],[13,16,10],[20,17,15]]) # inv mod 26 must be [8,5,10|21,8,21|21,12,8]
    #inv_A_mod26 = A.inv_mod(26)
    #print(inv_A_mod26)
    
    #inv_Am26 = NMatrix([[8,5,10],
    #                   [21,8,21],
    #                   [21,12,8], ])
    #p = A * inv_Am26                # p==identity matrix (mod 26)
    #
    #print(p.s_mod(26))
   
    pass
    



if __name__=='__main__':
    main()
    