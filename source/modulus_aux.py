# :filename: modulus_aux.py     auxiliary modulus functions
# ©2020 luciano de falco alfano
# under a CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/) license
# author disclaims any and all liability for any direct or indirect damages resulting
#   from errors of content or due to its use
# functions:
#     - lcg              pseudorandom numbers using a Linear Congruential Generator;
#                            attention: this returns a python generator, call "next" to get the number
#     - equiv_list       members of an equivalence class of remainders
#     - naive_invmod     inverse modulus, naive version
#     - egcd             extended euclidean algorithm (extended greatest common divisor)
#     - invmod           inverse modulus

def lcg(seed=0):
    '''pseudorandom numbers using a linear congruential generator
        
        param  seed       int - an initial value
        return a generator of float pseudorandom number in interval (0, 1]
        
        remark - constants are from wikipedia (https://en.wikipedia.org/wiki/Linear_congruential_generator) 
                     as glibc used by GCC
               - calculates pseudorandom number as Y_{i+1} = (a * Y_i + c ) mod m
    '''
    a = 1103515245
    c = 12345
    m = 2 << 31       # this is 2^31
    while True:
        seed = (a * seed + c) % m               # see remarks
        yield (seed & 0x3fffffff) / (2 << 29)   # last 30 bits, divided by 2^29 to adjust in interval (0,1]

def equiv_list(m, a=0, max_q=5):
    '''first 2*max_q+1 members of an equivalence class of remainders
       of modulus m
    
    params
      - m            int - modulus
      - a            int - 1st member; if a>m -> a=a%m
      - max_q        int - number half-1 of members to calculate
    
    return a list of 2*max_q+1 members
    
    note. members are calculated as a-q*m and a+q*m
    '''
    a = a % m
    result = []
    for q in range(0, max_q + 1):
        if q == 0:
            result.append(a)
        else:
            result.insert(0, a - q * m)
            result.append(a + q * m)
    return result


def naive_invmod(a, m): 
    '''modular multiplicative inverse of "a" (mod p), naive approach
       
       parameters
         - a            int - numer to inverse
         - m            int - modulus
       return mod.mult.inv. as int, if exists, else it raises ValueError
       note: derived from https://www.geeksforgeeks.org/multiplicative-inverse-under-modulo-m/
    '''
    a = a % m; 
    for x in range(1, m) : 
        if ((a * x) % m == 1) : 
            return x 
    raise ValueError(f"{a} doesn't have an inverse under modulo {m}")


def egcd(a, b):
    '''extended euclidean algorithm (extended greatest common divisor)
    
    params: a, b     int - numbers to get GCD
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

if __name__=='__main__':
    print( equiv_list(9, 3) )
