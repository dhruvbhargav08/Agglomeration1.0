from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView, Response
import home.RSA
import home.AES
import home.AffineCipher
import json

# Create your views here.
class RSA(APIView):
    def get(self, request):
        p = home.RSA.generate_large_prime()
        q = home.RSA.generate_large_prime()
        while p == q:
            q = home.RSA.generate_large_prime()
        auto = request.data["auto"]  # frontend input
        if not auto:
            p = request.data["p"]
            q = request.data["q"]
        public_key, private_key, n, phi, d, e = home.RSA.generate_keys(p, q)
        plaintext = request.data["plaintext"]
        ciphertext = home.RSA.encrypt(public_key, plaintext)
        decrypted_text = home.RSA.decrypt(private_key, ciphertext)
        data = {
            "p": p,
            "q": q,
            "n": n,
            "phi": phi,
            "d": d,
            "e": e,
            "public_key": public_key,
            "private_key": private_key,
            "ciphertext": ciphertext,
            "decrypted_text": decrypted_text,
            "plaintext": plaintext
        }
        response = {
            "success": True,
            "data": data,
        }
        return Response(response, status.HTTP_200_OK)


class AES(APIView):
    def get(self, request):
        # key = request.data["key"]
        # msg = request.data[key]
        key = request.data["key"]
        message = request.data["plaintext"]
        
        aes128 = home.AES.AES()
        encryption_result = aes128.encrypt(key, message)
        ciphertext = encryption_result['encrypted']
        decryption_result = aes128.decrypt(key, ciphertext)
        data = {
            "key": key,
            "message": message,
            "ciphertext": ciphertext,
            "decryption_result": decryption_result
        }
        response = {
            "success": True,
            "data": data,
        }
        return Response(response, status.HTTP_200_OK)
   
class AffineCipher(APIView):
    def get(self, request):
        a, b = 5, 11
        plaintext = request.data["plaintext"]
        encrypted_text, encryption_steps = home.AffineCipher.affine_encrypt(plaintext, a, b)
        decrypted_text, decryption_steps = home.AffineCipher.affine_decrypt(encrypted_text, a, b)
        data = {
            "encrypted_text": encrypted_text,  # Use repr for better representation of non-printable characters
            "decrypted_text": decrypted_text,
            "encryption_steps": encryption_steps,
            "decryption_steps": decryption_steps
        }
        print(data)
        data = json.dumps(data, indent = 4)
        response = {
            "success": True,
            "data": data,
        }
        return Response(response, status.HTTP_200_OK)
    