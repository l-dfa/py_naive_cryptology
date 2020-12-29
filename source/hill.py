# :filename: hill.py hill cipher

# import user libs
try:
    import nmatrix as nm
except:
    import source.nmatrix as nm

#alphabet = { 'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4,
#             'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9,
#             'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14,
#             'P': 15, 'Q': 16, 'R': 17, 'S': 18, 'T': 19,
#             'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25,
#           }
#plaintext = "ACT"
#key = nm.NMatrix([[6,24,1],[13,16,10],[20,17,15]])

#def get_key(d, val):
#    for k, v in d.items():
#        if v == val:
#            return k
#    raise ValueError('value not present')

def encrypt(plain, key):
    '''hill encrypt of plaintext to ciphertext
    
       params
         - plain         str - plaintext
         - key           NMatrix - the (numeric) key to encrypt
    
       return chiphertext as a string of chars
    '''
    
    numeric_p = chars2codes(plain)                           # 1. plaintext from chars to list of numbers
    
    segmented_np = segment_num(numeric_p, len(key))                    # 2. segmenting plaintext: list of lists
    
    numeric_cipher = encrypt_num(segmented_np, key, ord("Z")-ord("A")+1)          # 3. make ciphertext as list of lists of numbers
    
    numeric_cipher = [item for row in numeric_cipher for item in row]  # 4. flatting numeric ciphertext
    
    alpha_cipher = codes2chars(numeric_cipher)               # 5. decoding to chars

    return alpha_cipher

def decrypt(cipher, key):
    '''hill decrypt of plaintext to ciphertext
    
       params
         - cipher        str - ciphertext
         - key           NMatrix - the (numeric) key to encrypt
    
       return plaintext as a string of chars
    '''
    # 1. plaintext from chars to list of numbers
    numeric_p = chars2codes(cipher)
    # 2. segmenting ciphertext: list of lists
    segmented_nc = segment_num(numeric_p, len(key))
    # 3. make ciphertext as list of lists of numbers
    numeric_p = decrypt_num(segmented_nc, key, ord("Z")-ord("A")+1)
    # 4. flatting numeric plaintext
    numeric_p = [item for row in numeric_p for item in row]
    # 5. decoding to chars
    alpha_p = codes2chars(numeric_p)
    # done
    return alpha_p

def chars2codes(plain):
    '''coding from plaintext to list of numbers
    
       params
         - plain            str - a text to code as numbers
       return a list of numbers
       note. raise error if a char in plain is not key in alphabet
    '''
    p = plain.upper()         # ever uppercase text
    numeric_p = []
    for c in p:
        numeric_p.append(ord(c)-ord("A"))
    return numeric_p

def codes2chars(l):
    '''decoding from list of codes to string of chars'''
    alpha_cipher = []
    for e in l:
        alpha_cipher.append(chr(e+ord("A")))
    alpha_cipher = ''.join(alpha_cipher)
    return alpha_cipher

def segment_num(np, l):
    '''from a flat list to a list of lists, each row has length == to n.rows of key
    
       params
         - np     list - a flat list of codes
         - l      int - lenght of the key (square matrix)
       return a list of lists, each row has the same lenght of the nrow of key
       note if len(np) is not an int multiplier of nrow, remainder will be dropped
    '''
    if len(np) % l != 0:
        raise ValueError('plaintext lenght is not divisible by key lenght')
    segmented_np = []
    b = 0                             # base
    while b+l<=len(np):
        segmented_np.append(np[b:b+l])
        b += l
    return segmented_np

def encrypt_num(sn, key, mod):
    '''encrypt a segmented coded text 
    
       params
         - sn         list of lists - the coded text to encrypt
         - key        NMatrix - the key to use to encrypt
       return list of lists encrypted as code
    '''
    numeric_cipher = []
    for row in sn:
        vect = nm.NMatrix([row])         # matrix of single row
        vect = vect.t()                  # matrix of single column
        vect = key * vect
        vect = vect.s_mod(mod)           # cipher matrix of single column
        #print(vect)
        vect = vect.t()                  # now cipher matrix of single row
        numeric_cipher.append(vect.getr(0))
    return numeric_cipher

def decrypt_num(nc, key, mod):
    inv_key = key.inv_mod(mod)
    numeric_p = []
    for row in nc:
        vect = nm.NMatrix([row])
        vect = vect.t()                  # matrix of single column
        vect = inv_key * vect
        vect = vect.s_mod(mod) # cipher matrix of single column
        vect = vect.t()                  # now cipher matrix of single row
        numeric_p.append(vect.getr(0))
    return numeric_p

def main():
    #            123123123123   4*3
    plaintext = "paymoremoney"
    key = nm.NMatrix([[17, 17,  5],
                      [21, 18, 21],
                      [ 2,  2, 19],
                     ])
    print(f'plaintext: {plaintext}')
    print(f'key: {key}')

    ciphertext = encrypt(plaintext, key)
    print(f'ciphertext: {ciphertext}')
    
    invkey = key.inv_mod(ord("Z")-ord("A")+1)
    print(f'key^-1: {invkey}')
    
    ptext      = decrypt(ciphertext, key)
    ptext = ptext.lower()
    print(f'calculated plaintext: {ptext}')
    
    
if __name__=='__main__':
    main()