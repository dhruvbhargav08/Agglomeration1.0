import json


# Helper function to find modular inverse
def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None


# Affine cipher encryption (modified to handle all characters)
def affine_encrypt(text, a, b):
    m = 256  # Consider all ASCII characters
    encrypted_text = ""
    steps = []
    for char in text:
        x = ord(char)  # Get the ASCII value of the character
        encrypted_char = (a * x + b) % m  # Apply affine transformation
        encrypted_text += chr(encrypted_char)  # Convert back to character
        steps.append({
            "char": char,
            "x": x,
            "encrypted_value": encrypted_char,
            "encrypted_char": encrypted_text[-1]  # Use repr to represent non-printable characters
        })
    return encrypted_text, steps


# Affine cipher decryption (modified to handle all characters)
def affine_decrypt(text, a, b):
    m = 256  # Consider all ASCII characters
    a_inv = mod_inverse(a, m)
    if a_inv is None:
        raise ValueError(f"No modular inverse exists for a = {a} and m = {m}")
    
    decrypted_text = ""
    steps = []
    for char in text:
        y = ord(char)  # Get the ASCII value of the character
        decrypted_char = (a_inv * (y - b)) % m  # Apply inverse affine transformation
        decrypted_text += chr(decrypted_char)  # Convert back to character
        steps.append({
            "char": char,
            "y": y,
            "decrypted_value": decrypted_char,
            "decrypted_char": decrypted_text[-1] # Use repr to represent non-printable characters
        })
    
    return decrypted_text, steps