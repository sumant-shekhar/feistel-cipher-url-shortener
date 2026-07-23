import string

# Base62 alphabet
BASE62_ALPHABET = string.digits + string.ascii_lowercase + string.ascii_uppercase

# Simple Feistel Cipher for 32-bit integers
# This is a classic implementation that shows understanding of the concept.
FEISTEL_ROUNDS = 4
FEISTEL_KEY = 0xDEADBEEF  # A static key for the resume project
 
def feistel_round_function(val, key):
    """A simple round function: (val * key) XOR key"""
    return ((val * key) ^ (key >> 4)) & 0xFFFF

def encrypt_id(n):
    """Scrambles a 32-bit integer using a Feistel Cipher."""
    # Split 32-bit int into two 16-bit halves
    left = (n >> 16) & 0xFFFF
    right = n & 0xFFFF
    
    for i in range(FEISTEL_ROUNDS):
        # The core Feistel transformation
        temp = right
        right = left ^ feistel_round_function(right, FEISTEL_KEY)
        left = temp
        
    # Combine halves back (right first because of the last swap)
    return (left << 16) | right

def decrypt_id(n):
    """Descrambles a 32-bit integer back to its original value."""
    left = (n >> 16) & 0xFFFF
    right = n & 0xFFFF
    
    for i in range(FEISTEL_ROUNDS):
        # Reverse the rounds
        temp = left
        left = right ^ feistel_round_function(left, FEISTEL_KEY)
        right = temp
        
    return (left << 16) | right

def base62_encode(num):
    """Encodes a positive integer into a Base62 string."""
    if num == 0:
        return BASE62_ALPHABET[0]
    
    arr = []
    base = len(BASE62_ALPHABET)
    while num:
        num, rem = divmod(num, base)
        arr.append(BASE62_ALPHABET[rem])
    arr.reverse()
    return ''.join(arr)

def base62_decode(string):
    """Decodes a Base62 string into an integer."""
    base = len(BASE62_ALPHABET)
    num = 0
    for char in string:
        num = num * base + BASE62_ALPHABET.index(char)
    return num
