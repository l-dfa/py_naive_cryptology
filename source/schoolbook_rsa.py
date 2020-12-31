# :filename: schoolbook_rsa.py core of Rivest, Shamir, Adleman (RSA) cypher
# 
# documented by https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Operation
#
# steps: key generation
#        key distribution
#        encryption
#        decription


# import user libs
try:
    import numbers_ops as nops
except:
    import source.numbers_ops as nops


def keys(prime_len=10, p=None, q=None):
    '''
       args
           - prime_len      int - length in bits of random primes to generate
           - p, q           int - two prime numbers
       
       return (public_key, private_key,)   ((n, e,), (n, d,),) - generated keys
       
       rem. don't use prime_len < 6
    '''
    if prime_len < 6: raise ValueError("prime_len < 6")
    if p is not None and not nops.is_prime_mr(p): raise ValueError("p is not prime")
    if q is not None and not nops.is_prime_mr(q): raise ValueError("q is not prime")
    
    # key generation, see: https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Key_generation
    #    Choose at random two distinct prime numbers p and q. They should be similar in magnitude but differ in length by a few digits. p and q are secret
    if p is None:
        p = nops.generate_prime_number(length=prime_len)
    if q is None:
        q = nops.generate_prime_number(length=(prime_len + 8))          # +8 to get two more digits
    
    #    Compute n = pq. This is the modulus for both the public and private keys. n is released as part of the public key.    
    n = p * q
    
    #    Compute the Carmichael's totient function λ(n). It is λ(n) = lcm(p − 1, q − 1). λ(n) is kept secret. lcm is the "least common multiple"
    lambda_n = nops.lcm(p - 1, q - 1)

    #    Choose an integer e such that 1 < e < lambda_n and gcd(e, lambda_n) = 1; that is, they are coprime. the most used value is 2^16 + 1 = 65,537. e==3 is less secure. "e" is released as part of the public key
    min = 2 if lambda_n < 65537 else 65537
    cgen = nops.coprimes_gen(lambda_n, min=min)       # coprimes generator starting @ min, stopping @ lambda_n
    e = next(cgen)                                    # 1st coprime (usually 65537)

    #    Determine d as d ≡ e^−1 (mod lambda_n); that is, d is the modular multiplicative inverse of e modulo lambda_n. Use egcd(e, lambda_n) because they are coprime, so equation is a form of Bézout's identity, where d is one of the coefficients. d is kept secret as the private key exponent.
    _, d, _ = nops.egcd(e, lambda_n)

    return ((n, e,), (n, d,),)          # (public_key,  private_key, )


def encrypt(x, pub):
    '''encrypt x using public key
    
       args
           - x     int - < n coded plaintext
           - pub   (n, e,) - public key
       
       return ciphertext as int
    '''
    return pow(x, pub[1], pub[0])


def decrypt(y, pri):
    '''decrypt y using private key
    
       args
           - y     int - ciphertext
           - pri   (n, d,) - private key
       
       return plaintext as int
    '''
    return pow(y, pri[1], pri[0])


def main():
    public, private = keys()
    print(f"public key: {public}, private key: {private}")
    x = 2300
    y = encrypt(x, public)
    print(f"x: {x}, y: {y}")
    x = decrypt(y, private)
    print(f"y: {y}, x: {x}")   # INCREDIBLE: it's working!


if __name__ == '__main__':
    main()