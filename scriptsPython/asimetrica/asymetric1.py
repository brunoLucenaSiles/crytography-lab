import os
from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)
# hay que instalar el paquete pycryptodome
# pip install pycryptodome 

if __name__ == "__main__":
    key = os.urandom(32)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ct = encryptor.update(b"a secret message") + encryptor.finalize()
    print("Ciphertext:", ct)
    
    decryptor = cipher.decryptor()
    ct = decryptor.update(ct) + decryptor.finalize()
    
    print("Decrypted message:", ct)