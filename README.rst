py_naive_cryptology
=====================

Experimenting naive algorithms about cryptography, as a method to study them.

This will be a collection of scripts to test algoritms about (de)encrypting
with various technics.

implemented cryptology algorithms
-----------------------------------

Schoolbook **RSA** cipher. It in in module `schoolbook_rsa.py`. To use it, see `main()` in module.

**DES** cipher. It is in module `des.py`. To use it, see `main()` in module.

**Hill** cipher. It is in module `hill.py`.  To use it, see `main()` in module.

numbers_ops.py
-----------------

A module with auxiliary modulus functions, and others.

Main functions are:

.. code:: python

   import numbers_ops as nops
   
   nops.coprimes_gen(n,[min])            # coprime numbers (python) GENERATOR
   nops.coprimes(n,[min])                # list of coprime numbers
   nops.generate_prime_number([length])  # random generator of a single prime number
   nops.primes_gen([min],[max])          # prime numbers (python) GENERATOR
   nops.primes([min],[max])              # list of prime numbers
   nops.lcm(a,b)                         # least (or lowest) common multiple
   nops.gcd(a,b)                         # greatest common divisor
   nops.is_prime(n)                      # primality test
   nops.is_prime_mr(n)                   # Miller-Rabin: statistically primality test 
   nops.lcg([seed])                      # pseudorandom numbers using a Linear Congruential (python) GENERATOR
   nops.equiv_list(m,[a],[max_q])        # list of members of an equivalence class of remainders
   nops.naive_invmod(a, m)               # inverse modulus, naive version
   nops.egcd(a, b)                       # extended euclidean algorithm (extended greatest common divisor)
   nops.invmod(a, m)                     # inverse modulus

nbitarray.py
--------------

Naive pure python module to handle an array of bits.

It implements the class NBitArray. Its main methods are:

.. code:: python

   import nbitarray as nba
   
   ba = nba.NBitArray(list_of_hex)    # create instance
   bb = nba.NBitArray(list_of_bits)   # create instance
   len(ba)                            # number of bits
   ba[ndx]                            # bit at index ndx
   ba[ndx] = bit_as_integer           # set bit at index ndx
   ba == bb                           # eq operator
   str(ba)                            # string of bits
   ba + bb                            # concatenation operator
   ba ^ bb                            # xor operator (ba and bb have the same length)
   ba << n                            # left shift, note: ba.__lshift__(n, circular=True) does a circular left shift
   ba >> n                            # right shift, note: ba.__rshift__(n, circular=True) does a circular right shift
   ba.get_byte(bit_ndx|byte_ndx=)     # return one byte as integer from indicated position
   ba.set_byte(x, bit_ndx|byte_ndx=, lenght=)  # set x as one byte at indicated position for the indicated length in bits
   ba.permutate(permutation_table)  # return a permutated NBitArray obeying to the given permutation table. ...
                                    #  ... permutation table is a list of integers where index indicate the position of the output bit ...
                                    #  ... and value at the index is the position of the input bit.
   ba.bit_list()              # return the bit array content as a list of integers with values 0|1
   ba.hex()                   # return the bit array content as a string of hex numbers
   ba.swap_lr()               # return an NBitArray with left and right halves inverted. len(ba) must be even
   
nmatrix.py
-----------

This project contains a pure python module named `nmatrix.py`. The letter *n*
means *naive*. I have implemented it
to better understand and manage some basic mechanisms, to use in the
Hill's cipher.

It implements the class NMatrix. Its instances are matrix and it is a simple
implementation of the principal operations about matrix.

In short, main methods are:

.. code:: python
   
   import nmatrix as nm
   
   M  = nm.NMatrix(list_of_rows_each_as_list_of_numbers)   # create instance of matrix M by list of lists, one for each row
   I  = nm.NMatrix.identity(nrows)                         # create identity matrix I with nrows x ncols
   Zs = nm.NMatrix.zeros(nrows, [ncols])                   # create matrix of zeroes nrows x ncols (or nrows x nrows if ncols is not indicated)
   R  = nm.NMatrix.random(nrows, [ncols], [rands])         # create a matrix of random numbers get from the list "rands"
   M.nrows                             # number of rows
   M.ncols                             # number of columns
   M.shape                             # (nrows, ncols,)
   len(M)                              # nrows
   M.as_list_of_lists()                # return matrix as a list of lists
   M.copy()                            # ret a copy of matrix M
   M.is_square()                       # true if M is a square matrix
   M.det()                             # (weak) determinant of M
   M.rdet()                            # determinant of M by recursive algorithm, manage better zeros on main diagonal
   M.minor(nrow, ncol)                 # ret copy of M without "nrow" row and "ncol" column
   M[nrow, ncol] = number              # set number at M[nrow, ncol]==M[nrows][ncols]
   M[nrow]       = list_of_numbers     # set an entire row
   M.getc(ncol)                        # get column at index ncol
   M.setc(ncol, list_of_numbers)       # set column at index ncol with list of numbers
   A + B                               # sum of two matrices
   A - B                               # subtraction of two matrices
   A * B                               # multiplay of two matrices (remember: A*B != B*A)
   A.inv()                             # inverse of square matrix A, if it exists (it's I == A * A**-1)
   A / B                               # true division of two matrices, with A / B == A * B**-1, if B has an inverse
   A + b                               # sum of scalar b for each element of matrix A (scalar must be right operand)
   A - b                               # difference of scalar b for each element of matrix A (scalar must be right operand)
   A * b                               # multiply of scalar b for each element of matrix A (scalar must be right operand)
   A / b                               # true division of scalar b for each element of matrix A (scalar must be right operand)
   A // b                              # floor division of scalar b for each element of matrix A (scalar must be right operand)
   A % b                               # modulus b for each element of matrix A (modulus must be right operand)
   A.inv_mod(b)                        # modular b inversion of matrix A (it's A * (A**-1 mod b) == B mod b == I)
   A.round(n)                          # round each element of A, by n precision
   A.t()                               # transpose of A


Prerequisites of the development environment
---------------------------------------------

Base environments:

* `git <https://git-scm.com/downloads>`_
* `python <https://www.python.org/downloads/>`_ >= 3.8

No third parties libraries.

To install the development environment
----------------------------------------

In cmd::

  git clone https://github.com/l-dfa/py_naive_cryptology.git
  cd py_naive_cryptology
  
To exec application in development environment
-------------------------------------------------

In cmd::

  cd py_naive_cryptology\source
  python hill.py   # to run the hill (de)encyphering example
  
Test
--------------------

To run unit tests. In cmd::

  cd py_naive_cryptology\tests
  python -m unittest

License
----------

`CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0/>`_
