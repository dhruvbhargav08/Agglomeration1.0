from django.urls import path
from home.views import RSA, AES, AffineCipher

urlpatterns = [
    path("rsa", RSA.as_view()),
    path("aes", AES.as_view()),
    path("affinecipher", AffineCipher.as_view())
]
