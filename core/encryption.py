from Crypto.Cipher import AES, PKCS1_OAEP
import base64
import os
from Crypto.Protocol.KDF import PBKDF2
import jwt 
from Crypto.PublicKey import RSA 


def pad(byte_array): 
    block_size = 16 
    pad_len = block_size - len(byte_array) % block_size 
    return byte_array + (bytes([pad_len]) * pad_len) 


def unpad(byte_array):
    last_byte = byte_array[-1] 
    return byte_array[0:-last_byte] 


def aes_encrypt(message, iv, key):
    byte_array = message.encode("UTF-8") 
    padded = pad(byte_array) 
    key_iv = iv.encode("UTF-8") 
    cipher = AES.new(key.encode("UTF-8"), AES.MODE_CBC, key_iv) 
    encrypted_str = cipher.encrypt(padded) 
    return base64.b64encode(encrypted_str).decode("UTF-8") 


def aes_decrypt(message, iv, key):
    byte_array = base64.b64decode(message) 
    key_iv = iv.encode("UTF-8") 
    cipher = AES.new(key.encode("UTF-8"), AES.MODE_CBC, key_iv) 
    decrypted_padded = cipher.decrypt(byte_array) 
    decrypted_str = unpad(decrypted_padded) 
    return bytes.decode(decrypted_str)
