import socket
from hashlib import sha256
import time
from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)
import os
import ssl
def send_symmetric_message(iv, ciphertext):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 12346))
        s.sendall(iv+ciphertext)
        print("Message sent to Client A")

def exchangePrivateNumber(secretNumberA):
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_cert_chain(certfile="client.crt", keyfile="client.key")
    context.load_verify_locations("server.crt")  # Verifica el servidor

    with socket.create_connection(("localhost", 12345)) as sock:
        with context.wrap_socket(sock, server_hostname="localhost") as s:
            print("Safe connection established")
            s.sendall(str(secretNumberA).encode())
            print("Public number sent to B:", secretNumberA)
            data = s.recv(1024)
            numberFromB = int(data.decode())
            print("Public number received from B:", numberFromB)
            return numberFromB

def encrypt_aes(key, text):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CTR(iv))  # Usar CBC
    encryptor = cipher.encryptor()
    ct = encryptor.update(message.encode()) + encryptor.finalize()
    return iv, ct

if __name__ == "__main__":
    p = 23 # Prime number
    g = 5  # Primitive root modulo p

    privateKeyB= int(input("Enter a private number for A: "))
    publicKeyB = pow(g, privateKeyB, p)
    print("Key generated by A:", publicKeyB)

    publicKeyA = exchangePrivateNumber(publicKeyB)

    sharedPrivateKey = pow(publicKeyA, privateKeyB, p)
    print("Shared private key:", sharedPrivateKey)

    aes_key = sha256(str(sharedPrivateKey).encode()).digest()

    message = input("Enter the message to send to client A: ")

    time.sleep(1)

    iv, ciphertext = encrypt_aes(aes_key, message)

    send_symmetric_message(iv, ciphertext)

