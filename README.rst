py_naive_cryptology
=====================

Experimenting naive algorithms about cryptography, to study.

This will be a collection of scripts to test algoritms about (de)encrypting
with various technics.

implemented cryptology algorithms
-----------------------------------

**Hill** cipher. It is in module `hill.py`. To use it:

.. code:: python

   import hill as hill
   
   ciphertext = hill.encrypt(plaintext, keymatrix)
   plaintext  = hill.decrypt(ciphertext, keymatrix)

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
  python unit_tests.py

License
----------

`CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0/>`_
