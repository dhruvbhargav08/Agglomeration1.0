import random
from sympy import isprime, mod_inverse
import math


# Function to generate large prime numbers
def generate_large_prime():
    while True:
        prime = random.randint(100, 999)
        if isprime(prime):
            return prime


# RSA key generation
def generate_keys():
    p = generate_large_prime()
    print(f"Step 1: Generated first prime p = {p}")
    
    q = generate_large_prime()
    while q == p:  # Ensure p and q are different
        q = generate_large_prime()
    print(f"Step 2: Generated second prime q = {q}")
    
    n = p * q
    print(f"Step 3: Calculated n = p * q = {n}")
    
    phi = (p - 1) * (q - 1)
    print(f"Step 4: Calculated \u03d5(n) = (p-1) * (q-1) = {phi}")
    
    # Choose e
    e = random.randint(2, phi - 1)
    while math.gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)
    print(f"Step 5: Selected public exponent e = {e}, which is coprime with \u03d5(n)")
    
    # Calculate d
    d = mod_inverse(e, phi)
    print(f"Step 6: Calculated private exponent d = {d} using modular inverse of e and \u03d5(n)")
    
    return (e, n), (d, n), (p, q)


# RSA encryption
def encrypt(public_key, plaintext):
    e, n = public_key
    print(f"Step 7: Encrypting plaintext using public key (e = {e}, n = {n})")
    encrypted = []
    for char in plaintext:
        enc_val = (ord(char) ** e) % n
        print(f"Encrypting '{char}' (ASCII {ord(char)}) to {enc_val}")
        encrypted.append(enc_val)
    return encrypted


# RSA decryption
def decrypt(private_key, ciphertext):
    d, n = private_key
    print(f"Step 8: Decrypting ciphertext using private key (d = {d}, n = {n})")
    decrypted = []
    for char in ciphertext:
        dec_val = (char ** d) % n
        print(f"Decrypting {char} to ASCII {dec_val} ('{chr(dec_val)}')")
        decrypted.append(chr(dec_val))
    return ''.join(decrypted)


if __name__ == "__main__":
    # Key generation
    print("Key Generation:")
    public_key, private_key, (p, q) = generate_keys()
    print(f"Generated Keys: \nPublic Key: {public_key}\nPrivate Key: {private_key}\n")
    
    # Input plaintext
    plaintext = input("Enter the plaintext to encrypt: ")
    print(f"Step 9: Plaintext to encrypt: '{plaintext}'")
    
    # Encryption
    ciphertext = encrypt(public_key, plaintext)
    print(f"Ciphertext: {ciphertext}\n")
    
    # Decryption
    decrypted_text = decrypt(private_key, ciphertext)
    print(f"Decrypted Text: '{decrypted_text}'\n")
    
    print("RSA process completed.")
