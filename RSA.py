from random import choice
from math import gcd
from shlex import join


def is_prime(num):
    is_it = False
    for i in range(2, num):
        if num % i == 0:
            is_it = True
            break
        if (is_it == False) and (num != 1):
            return num


def generate_large_prime():
    prime_num = []
    for i in range(0, 100):
        random_num = list(range(1, 1000))
        prime = is_prime(choice(random_num))
        if prime != None:
            prime_num.append(prime)
            return prime_num


def generate_keys():
    prime_num = generate_large_prime()
    prime_list = []
    for k in prime_num:
        if k > 127:
            prime_list.append(k)

    p = choice(prime_list)
    q = choice(prime_list)

    n = p * q

    phi_n = (p - 1) * (q - 1)

    print("p = ", p)
    print("q = ", q)
    print("N = ", n)
    print("phi_n = ", phi_n)

    for i in range(1, n):
        if (i < n) and (gcd(i, phi_n) == 1):
            e_list = []
            e_list.append(i)
    e = choice(e_list)
    for i in range(1, n):
        d = i
        if ((e * d) % phi_n) == 1:
            d_list = []
            d_list.append(d)
            d = choice(d_list)
            print("e = ", e)
            print("d = ", d)
            return e, d, n


e, d, n = generate_keys()


def encryption(p, e, n):
    print("Public Key = ({},{})".format(n, e))
    PT_encode = []
    CT = []

    for i in p:
        PT_encode.append(ord(i))
    print("Plaintext (in ASCII) = ", PT_encode)

    for P in PT_encode:
        CT.append((P ** e) % n)
    print("Encryption of plaintext (in ASCII) = ", CT)
    return CT


plaintext = input("Enter the message you want to encrypt: ")
print("Plaintext = ", plaintext)

ciphertext = encryption(plaintext, e, n)


def decryption(c, d, n):
    print("Private Key = ({},{})".format(n, d))
    PT = []
    for C in c:
        PT.append(pow(c, d) % n)
    print("Decryption of cyphertext (in ASCII) = ", PT)
    plaintext = []
    for j in PT:
        plaintext.append(chr(j))
    print("Plaintext = ", "", join(plaintext))
    return plaintext


P = decryption(ciphertext, d, n)


def encryption(m, e, n):
    # Returns c = m^e * (mod n)
    if e == 0:
        return 1
    if e % 2 == 0:
        t = encryption(m, e // 2, n)
        return (t * t) % n
    else:
        t = encryption(m, e // 2, n)
        return m * (t ** 2 % n) % n


# c = encryption(m, e, n)
# print("Encrypted message: ", c)

# Decryption using Fast Modular Exponentiation Algorithm (recursively)
def decryption(c, d, n):
    # Returns m = c^d * (mod n)
    if d == 0:
        return 1
    if d % 2 == 0:
        t = decryption(c, d // 2, n)
        return (t * t) % n
    else:
        t = decryption(c, d // 2, n)
        return c * (t ** 2 % n) % n


# m = decryption(c, d, n)
# print("Decrypted message: ", m)

def main():
    key_size = 32
    e, d, n = generate_keys(key_size)
   

    msg = "some message"

    encrypted_msg = encryption(msg, e, n)
    decrypted_msg = decryption(encrypted_msg, d, n)

    print(f"Message: {msg}")
    print(f"e: {e}")
    print(f"d: {d}")
    print(f"n: {n}")
    print(f"Encrypted message: {encrypted_msg}")
    print(f"Decrypted message: {decrypted_msg}")


# Enter the message to be sent
M = 19070
 
# Signature is created by author
S = pow(ord(M),d) % n
 
#verify
# Author sends M and S both to reader
# Reader generates message M1 using the
# signature S, authors's public key e and product n.
M1 = pow(S,e) % n
 
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
