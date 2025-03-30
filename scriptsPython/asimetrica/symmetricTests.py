import os
from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)
import hashlib
# hay que instalar el paquete pycryptodome, cryptography
# pip install pycryptodome 
# pip install cryptography

def encrypt_decrypt_aes():
    key = os.urandom(32)
    iv = os.urandom(16)
    cipherEncryptor = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipherEncryptor.encryptor()
    ct = encryptor.update(b"a secret message") + encryptor.finalize()
    print("Ciphertext:", ct)
    
    cipherDecryptor = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipherDecryptor.decryptor()
    ct = decryptor.update(ct) + decryptor.finalize()
    
    print("Decrypted message:", ct)

def verificate_hash_messages():
    message1 = hashlib.md5(b'Hello world')
    print(message1.hexdigest())


    message2 = hashlib.md5(b'Hello world.')
    print(message1.hexdigest())

    if(message1.digest() == message2.digest()):
        print("The messages are the same")
    else:
        print("The messages are different")

def verificate_hash_files():    
    with open("file1.txt", "rb") as file:
        message1 = hashlib.md5(file.read())
        print(message1.hexdigest())

    with open("file2.txt", "rb") as file:
        message2 = hashlib.md5(file.read())
        print(message2.hexdigest())

    
    with open("file3.txt", "rb") as file:
        message3 = hashlib.md5(file.read())
        print(message3.hexdigest())

    if(message1.digest() == message2.digest()):
        print("The messages 1 and 2 are the same")
    else:
        print("The messages 1 and 2 are different")

    if message1.digest() == message3.digest():
        print("The messages 1 and 3 are the same")
    else:
        print("The messages 1 and 3 are different")

def generate_password_hashes():
    while True:
        password = input("Enter a password: ")
        if password == "exit":
            break
        else:
            hash = hashlib.md5(password.encode())
            print("Password:", password)
            print("Hash:", hash.hexdigest())
            with open("passwords.txt", "a") as file:
                file.write(password + " " + hash.hexdigest() + "\n")

if __name__ == "__main__":
    action = int(input("What do you want to do ?"))
    if action == 1:
        encrypt_decrypt_aes()
    elif action == 2:
        verificate_hash_messages()
    elif action == 3:
        verificate_hash_files()
    elif action == 4:
        generate_password_hashes()
    else:
        print("Invalid option")