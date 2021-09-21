import random

def is_prime(n):
    # returns True if n is prime
    # this method doesn't prove if the number is prime but proves that it's not not prime
    if n > 1:
        for i in range(2, n):
            if (n % i) == 0:
                return False
    else:
        return True

def generate_keys(key_size=1024):
    e = d = n = 0

    # Step 1: get prime numbers, p and q
    p = generate_prime(key_size)
    q = generate_prime(key_size)

    # Step 2: RSA modulus
    n = p * q

    # Step 3: totient
    phi_n = (p - 1) * (q - 1)

    # Step 4: choose e
    while True:
        e = random.randrange(2 ** (key_size - 1), (2 ** key_size) - 1)
        if (is_co_prime(e, phi_n)):
            break

    # Step 5: choose d
    # d is mod inv of e with respect to phi_n, e * d (mod phi_n) = 1
    d = modular_inverse(e, phi_n)

    return e, d, n

def generate_prime(key_size):
    # this returns a large prime number of key_size bits in size
    # Example: key_size = 4
    #   max 4 bit key = 1111 = 15 = (2^4) - 1
    #   min 4 bit key = 1000 = 8 = 2^(4 - 1)
    min_key = 2 ** (key_size - 1)
    max_key = (2 ** key_size) - 1
    while True:
        num = random.randrange(min_key, max_key)
        if (is_prime(num)):
            return num

def is_co_prime(p, q):
    # this returns True if gcd(p, q) is 1 aka relatively prime
    return gcd(p, q) == 1

def gcd(p, q):
    # this is the euclidean algorithm to find gcd of p and q
    while q:
        p, q = q, p % q
    return p

def modular_inverse(a, b):
    gcd, x, y = egcd(a, b)

    if x < 0:
        x += b
    return x

def egcd(a, b):
    s = 0; old_s = 1
    t = 1; old_t = 0
    r = b; old_r = a

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * r
        old_t, t = t, old_t - quotient * t

    # return gcd, x, y
    return old_r, old_s, old_t

#Encryption & Decryption
#Encryption using Fast Modular Exponentiation Algorithm (recursively)
def encryption(m, e, n):
    #Returns c = m^e * (mod n)
    if e == 0:
        return 1
    if e%2 == 0:
        t = encryption(m, e//2, n)
        return (t*t)%n
    else:
        t = encryption(m, e//2, n)
        return m *(t**2%n)%n
#c = encryption(m, e, n)
#print("Encrypted message: ", c)

#Decryption using Fast Modular Exponentiation Algorithm (recursively)
def decryption(c, d, n):
    #Returns m = c^d * (mod n)
    if d == 0:
        return 1
    if d%2 == 0:
        t = decryption(c, d//2, n)
        return (t*t)%n
    else:
        t = decryption(c, d//2, n)
        return c *(t**2%n)%n
#m = decryption(c, d, n)
#print("Decrypted message: ", m)

def main():
    key_size = 32
    e, d, n = generate_keys(key_size)

    msg = "some message"
   
    
    encrypted_msg = encrypt(e, n, msg)
    decrypted_msg = decrypt(d, n, encrypted_msg)

    print(f"Message: {msg}")
    print(f"e: {e}")
    print(f"d: {d}")
    print(f"n: {n}")
    print(f"Encrypted message: {encrypted_msg}")
    print(f"Decrypted message: {decrypted_msg}")



# Enter the message to be sent
M = 19070
 
# Signature is created by author
S = (M ** d) % n
 
#verify
# Author sends M and S both to reader
# Reader generates message M1 using the
# signature S, authors's public key e and product n.
M1 = (S**e) % n
 
#check authenticity
# If M = M1 only then reader accepts
# the message sent by author.
 
if M == M1:
    print("As M = M1, Accept the\
    message sent by author")
else:
    print("As M not equal to M1,\
    Do not accept the message\
    sent by author ")
if __name__ == "__main__":
    main()




# KEY GENERATION
# Step 1: Generate two large pseudo primes p and q (Fermat's test)
# Step 2: Calculate RSA modulus, N, which = p * q
# Step 3: Calculate the Euclidean totient, phi(N), which = (p - 1)(q - 1)
# Step 4: Choose e, a public key that will be used to encrypt data
#         that is relatively prime (shares no common denominator) with phi(N)
#         and is less than phi(N)
#         1 < e <= phi(N)
# Step 5: Calculate d, a private key that will be used to decrypt data
#         that is a modular multiplicative inverse of e over phi(N)
#         e * d (mod phi(N)) = 1
#   5.1: Euclidean Algorithm
#        a * x + b * y = 1 (book)
#        phi(N) * x + e * y = 1 (our case) this translates into ->
#        phi(N) = (x mod e) * e + y , (x mod e) is how many times e goes into phi(N), y is the remainder or constant
#        this modulus calculation is repeated until the constant = 1, then it stops, making y = 1 = gcd
#        this constant should be 1 because the numbers need to be co-prime
#   5.2: Back Substitution
#
# Example:
#   Step 1:
#       p = 11, e = 13
#   Step 2:
#       N = p * q = 143
#   Step 3:
#       phi(N) = (p - 1)(q - 1) = 120
#   Step 4:
#       7, 11, 13, 17 -> all options, prime numbers that don't share a common factor with 120 other than 1
#       e = 13
#   Step 5:
#       e * d (mod phi(N)) = 1
#    5.1: Euclidean Algorithm
#       phi(N) * x + e * y = 1
#       120 * x + 13 * y = 1
#         translate this into the following
#       phi(N) = (phi(N) mod e) * e + remainder
#       120 = 9 * 13 + 3
#         move e to the front and the remainder to e
#       13 = 4 * 3 + 1 <-repeat shift until remainder = 1
#    5.2 Back Substitution
#         We isolate the remainders in the equations above
#       1 = 13 - 4 * 3
#       3 = 120 - 9 * 13
#         combine the equations
#       1 = 13 - 4 * (120 - 9 * 13)
#         combine like terms, so how many 13's; 1+(-4)*(-9)=37
#       1 = 37 * 13 - 4 * 120
#       1 = 37(13) - 4(120) <- if 37 was negative we would add the totient back to it
#         d = 37, e = 13,
#
#   p = 11, q = 13, N = 14, phi(N) = 120, e = 13, d = 37
#
#
#
#
#
#  ENCRYPTION
#    c = m^e * (mod N)
#    Example:
#       plaintext = "Hi" = 72,105 in ASCII
#       c0 = 72^13 * (mod 143) = 7
#       c1 = 105^13 * (mod 143) = 58
#       ciphertext = 7,58
#  Decryption
#     m = c^d * (mod N)
#
#
#
# DIGITAL SIGNATURE
#Steps:
#   Imported the RSA library
#   Created function to open files
#   Run private key through the function
#   Open message and return data in it
#   Create stamp on file
#   Sugn the message with owners private key
#   Then save the signature in a file and print it
#


