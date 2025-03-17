from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
import os
from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)
import socket
from cryptography.hazmat.backends import default_backend
from hashlib import sha256
import time

def decrypt_aes(key, iv, ciphertext):
    cipher = Cipher(algorithms.AES(key), modes.CTR(iv))
    decryptor = cipher.decryptor()
    ct = decryptor.update(ciphertext) + decryptor.finalize()
    return ct.decode()

def receive_and_decrypt_message_symmetric():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', 12347))
        s.listen()
        print("Waiting for encrypted message...")
        conn, addr = s.accept()
        with conn:
            return conn.recv(1024)

def generate_keys_a():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096
        # Depending the size of the key, the encryption and decryption will be faster or slower
        # Also, the size of the key will determine the security of the key
        # Besides, the size of the key will determine the size of the encrypted message
    )
    public_key = private_key.public_key()
    return private_key, public_key


def pem_keys(private_key, public_key):
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    return public_pem, private_pem

def client_a_exchange():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # Create tcp socket
        s.bind(('localhost', 12345))  # Associate the socket with a specific network interface and port number
        s.listen()  # Put the socket into server mode and wait for a connection
        print("Waiting connection from client B...")

        conn, addr = s.accept()  # Accept a connection
        with conn:
            print(f"Connection established with {addr}")
            conn.sendall(public_pem_a)  # Send the public key to Client B
            client_b_public = conn.recv(1024)  # Receive the public key from Client B
            print("Public B key received:\n", client_b_public.decode())

            client_b_public_key = serialization.load_pem_public_key(
            client_b_public,
            backend=default_backend()
            )

            return client_b_public_key

def generate_signature(private_key):
    signature = private_key_a.sign(
        str(private_key).encode(),
        padding.PSS(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

def verify_signature(decrypted_data, client_b_public):
    key_from_b, signature = decrypted_data.split(b"||SIGNATURE||") 

    try:
        client_b_public.verify(
            signature,  # Firma a verificar
            key_from_b,    # Mensaje original
            padding.PSS(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH  # Longitud del salt
            ),
            hashes.SHA256()  # Algoritmo hash utilizado
        )
        print("The firm is valid:", key_from_b.decode())
    except Exception as e:
        print("The firm is not valid:", e)
        
    return key_from_b

def send_encrypted_number(private_key_a,encrypted_blocks):
    encrypted_message_parts = []
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        time.sleep(2)
        s.connect(('localhost', 12346))  # Channel 2
        for block in encrypted_blocks:
            print(len(block))
            print("Enviando chunck")
            s.sendall(block)
            time.sleep(0.25)

        print("Message sent to Client B")
        s.sendall(b'end')
        print("Message vacio to Client B")
        while True:
            part = s.recv(512)
            if not part:
                break
            print("Message received ")
            print(len(part))
            encrypted_message_parts.append(part)

        decrypted_data = b""
        for encrypted_part in encrypted_message_parts:
            decrypted_part = private_key_a.decrypt(
                encrypted_part,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            decrypted_data += decrypted_part

        print("Decrypted message received")
        return decrypted_data
    

def receive_and_decrypt_message_asymmetric(private_key_a):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', 12346))
        s.listen()
        print("Waiting for encrypted message...")
        conn, addr = s.accept()
        with conn:
            encrypted_message_parts = []
            while True:
                part = conn.recv(1024)
                if not part:
                    break
                encrypted_message_parts.append(part)

            decrypted_data = b""
            for encrypted_part in encrypted_message_parts:
                decrypted_part = private_key_a.decrypt(
                    encrypted_part,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                decrypted_data += decrypted_part

            print("Decrypted message received")
            return decrypted_data

def encrypt_message(key_generated, signature, client_b_public):
    chunk_size = 214
    data_to_encrypt = str(key_generated).encode() + b"||SIGNATURE||" + signature
    encrypted_blocks = []

    # Divide the message in chunks
    for i in range(0, len(data_to_encrypt), chunk_size):
        chunk = data_to_encrypt[i:i + chunk_size]
            
        # Cypher the chunk
        encrypted_chunk = client_b_public.encrypt(
            chunk,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        encrypted_blocks.append(encrypted_chunk) 
        
    return encrypted_blocks


if __name__ == "__main__":

    private_key_a, public_key_a = generate_keys_a()

    public_pem_a, private_pem_a = pem_keys(private_key_a, public_key_a)
    
    #print("Private key:\n", public_pem_a.decode())
    #print("Public key:\n", private_pem_a.decode())
    
    client_b_public = client_a_exchange()
    #print("Client B public key:", client_b_public)
    
    print("I got the public key from B")

    p = 23 # Prime number
    g = 5  # Primitive root modulo p
    
    private_number_a = os.urandom(16)
    secret_number_a = pow(g, int.from_bytes(private_number_a, "big"), p)
    print("Key generated by A:", secret_number_a)
    
    signature = generate_signature(private_key_a)
    encrypted_blocks = encrypt_message(secret_number_a, signature, client_b_public)
    
    time.sleep(1)
    decrypted_data = send_encrypted_number(private_key_a,encrypted_blocks)
    
    #decrypted_data = receive_and_decrypt_message_asymmetric(private_key_a)
    
    key_generated_from_b = verify_signature(decrypted_data,client_b_public)
    
    print("Key generated by B:", key_generated_from_b.decode())
 
    private_key = pow(int(key_generated_from_b.decode()), int.from_bytes(private_number_a, "big"), p)
    
    print("Private key:", private_key)
    aes_key = sha256(str(private_key).encode()).digest()
    

    encripted_data = receive_and_decrypt_message_symmetric()

    print("Encrypted message:", encripted_data)
    iv = encripted_data[:16]
    ciphertext = encripted_data[16:]
    decrypted_message = decrypt_aes(aes_key, iv, ciphertext)
    print("Decrypted message:", decrypted_message)