from random import choice
from math import gcd
from shlex import join


def is_prime(num):
    yes_it_is = False
    for i in range(2, num):
        if num % i == 0:
            yes_it_is = True
            break
        if (yes_it_is == False) and (num != 1):
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
        if k > 127: # This is the last value of ASCII
            prime_list.append(k)

    # Step 1: Generate two large pseudo primes p and q (Fermat's test)
    p = choice(prime_list)
    q = choice(prime_list)

    # Step 2: Calculate RSA modulus, N, which = p * q
    n = p * q

    # Step 3: Calculate the Euclidean totient, phi(N), which = (p - 1)(q - 1)
    phi_n = (p - 1) * (q - 1)

    print("p = ", p)
    print("q = ", q)
    print("n = ", n)
    print("phi_n = ", phi_n)

    # Step 4: Choose e, a public key that will be used to encrypt data
    #         that is relatively prime (shares no common denominator) with phi(N)
    #         and is less than phi(N)
    #         1 < e <= phi(N)
    for i in range(1, n):
        if (i < n) and (gcd(i, phi_n) == 1):
            e_list = []
            e_list.append(i)
    e = choice(e_list)

    # Step 5: Calculate d, a private key that will be used to decrypt data
    #         that is a modular multiplicative inverse of e over phi(N)
    #         e * d (mod phi(N)) = 1
    #   5.1: Euclidean Algorithm
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
    p_text = []
    c_text = []
    # gives ASCII value of each character of the plaintext and stores it in p_text list
    for i in p:
        p_text.append(ord(i))
    print("Plaintext (in ASCII) = ", p_text)
    # retrieves elements one by one and compute cipher storing it in c_text list
    for P in p_text:
        c_text.append((P ** e) % n)
    print("Encryption of plaintext (in ASCII) = ", c_text)
    return c_text


plaintext = input("Enter the message you want to encrypt: ")
print("Plaintext = ", plaintext)

ciphertext = encryption(plaintext, e, n)


def decryption(c, d, n):
    print("Private Key = ({},{})".format(n, d))
    ptext = []
    # retrieves each character from ciphertext list (c) and computes plaintext storing in plaintext list
    for C in c:
        ptext.append((c ** d) % n)
    print("Decryption of cyphertext (in ASCII) = ", ptext)
    plaintext = []
    # converts ASCII number in plaintext to an alphabet character
    for j in ptext:
        plaintext.append(chr(j))
    # combines the alphabet characters together into one string
    print("Plaintext = ", "", join(plaintext))
    return plaintext

P = decryption(ciphertext, d, n)

def main():
    privkey = e

    msg = ""

    encrypted_msg = encryption(msg, e, n)
    decrypted_msg = decryption(encrypted_msg, d, n)



import rsa


def file_open(file):
    key_file = open(file, 'rb')
    key_data = key_file.read()
    key_file.close()
    return key_data


# Open private key file and load in key
e = rsa.PrivateKey.load_pkcs1(file_open('privatekey.key'))

# Open the secret message file and return data to variable
message = file_open('message')

# Sign the message with the owners private key
signature = rsa.sign(message, e, 'SHA-512')

s = open('signature_file', 'wb')
s.write(signature)

print(signature)
print(len(signature))


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
# Steps:
#   Imported the RSA library
#   Created function to open files
#   Run private key through the function
#   Open message and return data in it
#   Create stamp on file
#   Sugn the message with owners private key
#   Then save the signature and print it
#
