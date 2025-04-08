import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)

import sys

def encrypt_aes(text, key, iv):
    # Pad the text to be a multiple of the block size
    padder = padding.PKCS7(128).padder()  # 128 bits = 16 bytes
    padded_text = padder.update(text) + padder.finalize()

    # Create a cipher object using the key and IV
    cipherEncryptor = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipherEncryptor.encryptor()

    # Encrypt the padded text
    ct = encryptor.update(padded_text) + encryptor.finalize()
    print("Ciphertext:", ct)
    return ct

def decrypt_aes(text, key, iv):

    # Create a cipher object using the key and IV
    cipherDecryptor = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipherDecryptor.decryptor()

    # Decrypt the text
    decrypted_text  = decryptor.update(text) + decryptor.finalize()

    # Unpad the decrypted text
    unpadder = padding.PKCS7(128).unpadder()  # 128 bits = 16 bytes
    unpadded_text = unpadder.update(decrypted_text) + unpadder.finalize()

    decrypted_message = unpadded_text.decode('utf-8')
    
    print("Decrypted message:", decrypted_message)
    return decrypted_message


if __name__ == "__main__":
    if(len(sys.argv) != 3):
        print("Usage: python activity1.py <functionName> <filename>")
        sys.exit(1)

    functionName = sys.argv[1]
    filename = sys.argv[2]

    if os.path.exists("key_iv.txt"):
        with open("key_iv.txt", "rb") as file:
            key, iv = file.read(32), file.read(16)
    else:
        key = os.urandom(32)
        iv = os.urandom(16)

        # Guardar la clave y el IV en un archivo para usarlos luego
        with open("key_iv.txt", "wb") as file:
            file.write(key + iv)

    
    if(functionName == "encrypt"):
        with open(filename, "rb") as file:  
            text = file.read()

        encrypted_text = encrypt_aes(text, key, iv)

        with open("aes-encrypted.txt", "wb") as file:
            file.write(encrypted_text)

    elif(functionName == "decrypt"):
        with open(filename, "rb") as file:
            ct = file.read()
    
        decrypted_text = decrypt_aes(ct, key, iv)

        with open("aes-decrypted.txt", "w", encoding="utf-8") as file:
            file.write(decrypted_text)
    else:
        print("Function not found")
        sys.exit(1)
