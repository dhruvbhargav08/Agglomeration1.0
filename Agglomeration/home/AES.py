import json
import numpy as np
from base64 import b64encode, b64decode
from home.Aes_converter import keyToHexArray, arrayShift, arraySbox, xorArray, addRoundKey, subBytes, shiftRow, mixColumn
from home.Aes_converter import hexToMatrix, inverseMixColumn


class AES:
    def __init__(self):
        self.ROUND = 10
        self.ORDER = 4
        self.ROUNDKEY = []
        self.encryption_details = []  # Store encryption round details
        self.decryption_details = []  # Store decryption round details

    def __keySchedule(self, KEY):
        hexKey = keyToHexArray(KEY)
        self.ROUNDKEY.append(hexKey.tolist())
        for i in range(0, self.ROUND):
            prev_arr = np.array(self.ROUNDKEY[-1])
            last_col = prev_arr[self.ORDER - 1]
            shift_col = arrayShift(last_col)
            sbox_col = arraySbox(shift_col)
            col_1 = xorArray(prev_arr[0], sbox_col, i)
            col_2 = xorArray(col_1, prev_arr[1])
            col_3 = xorArray(col_2, prev_arr[2])
            col_4 = xorArray(col_3, prev_arr[3])
            new_arr = np.array([col_1, col_2, col_3, col_4])
            self.ROUNDKEY.append(new_arr.tolist())

    def __encryptProcess(self, TEXT):
        hexData = keyToHexArray(TEXT)
        cipher_arr = addRoundKey(hexData, np.array(self.ROUNDKEY[0]))
        self.encryption_details.append({
            "round": 0,
            "input": hexData.tolist(),
            "round_key": self.ROUNDKEY[0],
            "output": cipher_arr.tolist(),
        })

        for i in range(1, self.ROUND + 1):
            arr = cipher_arr
            sub_bytes_arr = subBytes(arr)
            shift_row_arr = shiftRow(sub_bytes_arr)
            mix_col_arr = mixColumn(shift_row_arr) if i != self.ROUND else shift_row_arr
            round_key_arr = np.array(self.ROUNDKEY[i])
            final_arr = addRoundKey(mix_col_arr, round_key_arr)

            # Store round details
            self.encryption_details.append({
                "round": i,
                "input": arr.tolist(),
                "sub_bytes": sub_bytes_arr.tolist(),
                "shift_row": shift_row_arr.tolist(),
                "mix_column": mix_col_arr.tolist() if i != self.ROUND else None,
                "round_key": self.ROUNDKEY[i],
                "output": final_arr.tolist(),
            })

            cipher_arr = final_arr
        return cipher_arr

    def __decryptProcess(self, CIPHER_HEX):
        hexData = hexToMatrix(CIPHER_HEX)
        plain_arr = addRoundKey(hexData, np.array(self.ROUNDKEY[-1]))
        self.decryption_details.append({
            "round": self.ROUND,
            "input": hexData.tolist(),
            "round_key": self.ROUNDKEY[-1],
            "output": plain_arr.tolist(),
        })

        for i in range(self.ROUND - 1, -1, -1):
            arr = plain_arr
            shift_row_arr = shiftRow(arr, left=False)
            sub_bytes_arr = subBytes(shift_row_arr, inverse=True)
            round_key_arr = np.array(self.ROUNDKEY[i])
            add_round_arr = addRoundKey(sub_bytes_arr, round_key_arr)
            mix_col_arr = inverseMixColumn(add_round_arr) if i != 0 else add_round_arr

            # Store round details
            self.decryption_details.insert(0, {
                "round": i,
                "input": arr.tolist(),
                "shift_row": shift_row_arr.tolist(),
                "sub_bytes": sub_bytes_arr.tolist(),
                "round_key": self.ROUNDKEY[i],
                "output": mix_col_arr.tolist() if i != 0 else add_round_arr.tolist(),
            })

            plain_arr = mix_col_arr
        return plain_arr

    def __addPadding(self, data):
        bytes_per_block = 16
        padded_data = []
        while len(data) > bytes_per_block:
            padded_data.append(data[:bytes_per_block])
            data = data[bytes_per_block:]
        padding_len = bytes_per_block - len(data)
        padded_data.append(data + chr(padding_len) * padding_len)
        return padded_data

    def __delPadding(self, data):
        padding_len = data[-1]
        if padding_len >= 1 and padding_len <= 16:
            return data[:-padding_len]
        return data

    def encrypt(self, KEY, TEXT):
        text_arr = self.__addPadding(TEXT)
        self.__keySchedule(KEY)
        hex_encrypt = ""
        for block in text_arr:
            cipher_matrix = self.__encryptProcess(block)
            cipher_text = list(np.array(cipher_matrix).reshape(-1,))
            for value in cipher_text:
                hex_encrypt += f"{value:02x}"
        self.ROUNDKEY = []  # Reset for security after processing
        return {
            "encrypted": hex_encrypt,
            "encryption_details": self.encryption_details
        }

    def decrypt(self, KEY, CIPHER_HEX):
        self.__keySchedule(KEY)
        plain_text = ""
        if len(CIPHER_HEX) % 32 != 0 or len(CIPHER_HEX) == 0:
            raise ValueError("Invalid cipher length. Must be non-empty and a multiple of 32 characters.")

        while CIPHER_HEX:
            cipher_block = CIPHER_HEX[:32]
            CIPHER_HEX = CIPHER_HEX[32:]
            plain_matrix = self.__decryptProcess(cipher_block)
            plain_arr = list(np.array(plain_matrix).reshape(-1,))
            plain_arr = self.__delPadding(plain_arr) if not CIPHER_HEX else plain_arr
            for char in plain_arr:
                plain_text += chr(char)
        self.ROUNDKEY = []  # Reset for security after processing
        return {
            "decrypted": plain_text,
            "decryption_details": self.decryption_details
        }


if __name__ == '__main__':

    aes128 = AES()

    # Define key and message

    # Encrypt the message
    encryption_result = aes128.encrypt(key, msg)
    # Decrypt the message
    ciphertext = encryption_result['encrypted']
    decryption_result = aes128.decrypt(key, ciphertext)