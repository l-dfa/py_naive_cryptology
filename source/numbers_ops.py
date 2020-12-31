# :filename: numbers_ops.py     auxiliary functions: modulus, primes, ...
# ©2020 luciano de falco alfano
# under a CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/) license
# author disclaims any and all liability for any direct or indirect damages resulting
#   from errors of content or due to its use
#
# functions:
#     - generate_prime_number  random generator of a single prime number
#     - primes_gen             prime numbers generator
#     - primes                 list of prime numbers
#     - lcm                    least (or lowest) common multiple
#     - gcd                    greatest common divisor
#     - is_prime               primality test
#     - is_prime_mr            Miller-Rabin: statistically primality test 
#     - lcg                    pseudorandom numbers using a Linear Congruential Generator;
#                                  attention: this returns a python generator, call "next" to get the number
#     - equiv_list             members of an equivalence class of remainders
#     - naive_invmod           inverse modulus, naive version
#     - egcd                   extended euclidean algorithm (extended greatest common divisor)
#     - invmod                 inverse modulus

# import std libs
from random import randrange
from secrets import randbits


def coprimes_gen(n, min=2):
    '''coprime numbers generator'''
    if min < 2 or min >= n: raise ValueError(f"min < 2 or min >= n") # min coprime is 2
    i = min
    while i <= n:
        if is_coprime(i, n):
            yield i
        i += 1


def coprimes(n, min=3):
    '''list of coprime numbers'''
    return list(coprimes_gen(n, min=min))


def primes_gen(min=2, max=100):
    '''prime numbers generator'''
    if min <= 1 or max < min: raise ValueError(f"min <= 1 or max < min") # 1 isn't prime
    i = min
    while i <= 3:                      # 2, 3 are prime
        yield i
        i += 1
    if i % 2 == 0:
        i += 1
    while i <= max:
        if is_prime(i):
            yield i
        i += 2


def is_prime_mr(n, k=128):
    """Test if a number is prime, Miller-Rabin
       
       Args:
           n -- int -- the number to test
           k -- int -- the number of tests to do
       
       return True if n is prime
       
       rem. from https://medium.com/@prudywsh/how-to-generate-big-prime-numbers-miller-rabin-49e6e6af32fb
    """
    # Test if n is not even.
    # But care, 2 is prime !
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    # find r and s
    s = 0
    r = n - 1
    while r & 1 == 0:
        s += 1
        r //= 2
    # do k tests
    for _ in range(k):
        a = randrange(2, n - 1)
        x = pow(a, r, n)
        if x != 1 and x != n - 1:
            j = 1
            while j < s and x != n - 1:
                x = pow(x, 2, n)
                if x == 1:
                    return False
                j += 1
            if x != n - 1:
                return False
    return True


def is_prime(n):
    '''Primality test
    
    params n     int - a positive integer
    
    return True|False
    
    remark.  using 6k+-1 optimization, from https://en.wikipedia.org/wiki/Primality_test
             for a fast test on large numbers use "is_prime_mr"
             timing of this function on i7-6500U@2.5GHz (MS Windows 10), with length of "n" in bits:
                 - 32 bits   ~     0.01 s
                 - 50 bits   ~     6 s
                 - 64 bits   ~   986 sec  (more of 15 minutes)
    '''
    if n <= 1: raise ValueError(f"argument <= 1")
    if n <= 3:                      # 2, 3 are prime, 1 is not
        return n > 1
    if n % 2 == 0 or n % 3 == 0:    # divisible by 2 or 3: not prime
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0: 
            return False
        i += 6
    return True


def is_coprime(a, b):
    return True if gcd(a, b) == 1 else False
    
def primes(min=2, max=100):
    '''return a list of prime numbers in the indicated range'''
    return list(primes_gen(min=min, max=max))


def generate_prime_candidate(length):
    """ Generate an odd integer randomly
    
        Args:
            length -- int -- the length of the number to generate, in bits

        return an integer
        
        rem. from https://medium.com/@prudywsh/how-to-generate-big-prime-numbers-miller-rabin-49e6e6af32fb
    """
    # generate random bits
    p = randbits(length)
    # apply a mask to set MSB and LSB to 1
    p |= (1 << length - 1) | 1
    return p


def generate_prime_number(length=1024):
    """ Generate a prime

        Args:
            length -- int -- length of the prime to generate, in bits

        return a prime
        
        rem. from https://medium.com/@prudywsh/how-to-generate-big-prime-numbers-miller-rabin-49e6e6af32fb
    """
    p = 4
    # keep generating while the primality test fail
    while not is_prime_mr(p):
        p = generate_prime_candidate(length)
    return p


def lcm(a, b):
    '''Least (or lowest) Common Multiple
    
    params a, b      int - numbers to use
    
    return an int as the lowest common multiple of ints "a" and "b"
    
    remark. from https://en.wikipedia.org/wiki/Least_common_multiple#Using_the_greatest_common_divisor
    '''
    return (a // gcd(a, b)) * b


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
    if a < 0 or b < 0:
        raise ValueError(f"there is a negative argument")
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def gcd(a, b):
    '''euclidean algorithm to Greatest Common Divisor
    
    params a, b    int - both >0, integers to discover gcd
    
    return the gcd as an int
    
    remark. from https://en.wikipedia.org/wiki/Euclidean_algorithm
    '''
    if a < 0 or b < 0:
        raise ValueError(f"there is a negative argument")
    while b != 0:
        t = b
        b = a % b
        a = t
    return a


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


def main():
    pass
#    #p = [ap for ap in primes_gen(min=10000, max=100000)]
#    #print(p[:10], len(p))
    import timeit
    
    # timing test for prime of a number with 64 bits
    print(timeit.timeit(stmt='''
b = numbers_ops.is_prime(p)
print(f"{b}")
''', setup='''
import numbers_ops
p = numbers_ops.generate_prime_number(length=64)
print(f"prime {p}")
''', number=1))
    print(f'seconds to test a prime with 64 bits')

#    # timing to generate primes from 10000 to 1000000 (77269 numbers)
#    print(timeit.timeit(stmt='''
#p = nops.primes(min=10000,max=1000000)
#print(f'seconds to generate {len(p)} primes from 10000 to 1000000:')
#''', setup='''
#import numbers_ops as nops
#''', number=1))

#    # timing to generate randomly 77269 primes using 20 bits
#    print(timeit.timeit(stmt='''
#c = 0
#while c < 77269:
#    p = nops.generate_prime_number(length=20)
#    c += 1
#print(f'seconds to generate randomly 77269 primes with 20 bits:')
#''', setup='''
#import numbers_ops as nops
#''' number=1))
    

if __name__=='__main__':
    main()
