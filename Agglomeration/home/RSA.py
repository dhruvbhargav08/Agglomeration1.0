import random
from sympy import mod_inverse
import math
from Crypto.Util import number


# Function to generate large prime numbers
def generate_large_prime():
    prime = number.getPrime(2048)
    return prime


# RSA key generation
def generate_keys(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    # Choose e
    e = random.randint(2, phi - 1)
    while math.gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)
    # Calculate d
    d = mod_inverse(e, phi)
    return (e, n), (d, n), n, phi, d, e


# RSA encryption
def encrypt(public_key, plaintext):
    e, n = public_key
    encrypted = []
    for char in plaintext:
        enc_val = (ord(char) ** e) % n
        encrypted.append(enc_val)
    return encrypted


# RSA decryption
def decrypt(private_key, ciphertext):
    d, n = private_key
    decrypted = []
    for char in ciphertext:
        dec_val = (char ** d) % n
        decrypted.append(chr(dec_val))
    return ''.join(decrypted)
