from Crypto.Util.Padding import pad, unpad

# Example S-Box (simplified for demonstration)
S_BOX = [
    [[14, 4, 13, 1], [2, 15, 11, 8], [3, 10, 6, 12], [5, 9, 0, 7]],
    [[0, 15, 7, 4], [14, 2, 13, 1], [10, 6, 12, 11], [9, 5, 3, 8]]
]


def print_step(title, data):
    print(f"\n=== {title} ===")
    print(data)


def initial_permutation(data):
    # Simplified permutation for demonstration
    permuted = data[::-1]  # Reverse bits as a simple example
    print_step("Initial Permutation", permuted)
    return permuted


def expansion_function(right_half):
    # Simple bit expansion (duplicating bits as an example)
    expanded = right_half + right_half[:4]
    print_step("Expansion Function", expanded)
    return expanded


def xor_operation(data, key):
    xored = ''.join('1' if bit1 != bit2 else '0' for bit1, bit2 in zip(data, key))
    print_step("XOR with Key", xored)
    return xored


def substitution(data):
    # Apply S-Box substitution
    blocks = [data[i:i + 4] for i in range(0, len(data), 4)]
    substituted = ''
    for i, block in enumerate(blocks):
        row = int(block[0] + block[-1], 2)
        col = int(block[1:3], 2)
        substituted += format(S_BOX[i % len(S_BOX)][row][col], '04b')
    print_step("Substitution", substituted)
    return substituted


def permutation(data):
    # Simple permutation (reverse for demonstration)
    permuted = data[::-1]
    print_step("Permutation", permuted)
    return permuted


def des_encrypt(plaintext, key):
    print_step("Plaintext", plaintext)
    print_step("Key", key)
    
    # Step 1: Initial Permutation
    permuted = initial_permutation(plaintext)
    
    # Split into left and right halves
    left, right = permuted[:len(permuted) // 2], permuted[len(permuted) // 2:]
    print_step("Left Half", left)
    print_step("Right Half", right)
    
    # Round Function (1 round for demonstration)
    for round_num in range(1, 2):  # Single round for simplicity
        print(f"\n--- Round {round_num} ---")
        expanded_right = expansion_function(right)
        xored = xor_operation(expanded_right, key)
        substituted = substitution(xored)
        permuted_right = permutation(substituted)
        new_right = ''.join('1' if bit1 != bit2 else '0' for bit1, bit2 in zip(permuted_right, left))
        left, right = right, new_right
        print_step("New Left", left)
        print_step("New Right", right)
    
    # Combine halves and apply final permutation
    combined = left + right
    final_permuted = combined[::-1]  # Simplified final permutation
    print_step("Final Permutation", final_permuted)
    return final_permuted


# Get User Input
plaintext = input("Enter plaintext in binary (e.g., 1010101111001101): ").strip()
key = input("Enter key in binary (16 bits, e.g., 0101110101110101): ").strip()

# Validate Input
if len(plaintext) != 16 or not all(bit in "01" for bit in plaintext):
    print("Invalid plaintext! Ensure it's 16 bits of binary.")
    exit()
if len(key) != 16 or not all(bit in "01" for bit in key):
    print("Invalid key! Ensure it's 16 bits of binary.")
    exit()

# Encrypt and Visualize Steps
ciphertext = des_encrypt(plaintext, key)

print("\nCiphertext:", ciphertext)
