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

def send_symmetric_message(iv, ciphertext):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 12347))
        s.sendall(iv+ciphertext)
        print("Message sent to Client A")


def encrypt_aes(key, text):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CTR(iv))  # Usar CBC
    encryptor = cipher.encryptor()
    ct = encryptor.update(message.encode()) + encryptor.finalize()
    return iv, ct

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

def client_b_exchange():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 12345))
        s.sendall(public_pem_b)  # Send public key to A
        client_a_public = s.recv(1024)  # Receive public key from A
        print("Public A key received:\n", client_a_public.decode())
        
        
        client_a_public_key = serialization.load_pem_public_key(
            client_a_public,
            backend=default_backend()
        )
        

        return client_a_public_key

def generate_signature(private_key):
    signature = private_key.sign(
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

def send_encrypted_message(encrypted_blocks):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('localhost', 12346))  # Channel 2
        for block in encrypted_blocks:
            print(len(block))
            s.sendall(block)
        
        print("Message sent to Client B")
        

def receive_and_decrypt_message(private_key_b,encrypted_blocks):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', 12346))
        s.listen()
        print("Waiting for encrypted message...")
        conn, addr = s.accept()
        with conn:
            encrypted_message_parts = []
            while True:
                part = conn.recv(512)
                if len(part) < 512:
                    print("End of message. Sending message to Client A")
                    break
                print("Message received ")
                print(len(part))
                encrypted_message_parts.append(part)

            print("Decrypted message received")
            decrypted_data = b""
            for encrypted_part in encrypted_message_parts:                
                decrypted_part = private_key_b.decrypt(
                    encrypted_part,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                decrypted_data += decrypted_part
                
            
            time.sleep(1)
            for block in encrypted_blocks:
                print(len(block))
                print("Enviando chunck")
                conn.sendall(block)
                time.sleep(0.5)
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
        print(len(encrypted_chunk))
        encrypted_blocks.append(encrypted_chunk) 
        
    return encrypted_blocks


if __name__ == "__main__":

    # Generate keys
    private_key_b, public_key_b = generate_keys_a()

    public_pem_b, private_pem_b = pem_keys(private_key_b, public_key_b)
    
    #print("Private key:\n", public_pem_b.decode())
    #print("Public key:\n", private_pem_b.decode())
    
    # Exchange keys
    client_a_public = client_b_exchange()
    
    print("I got the public key from A")
    
    p = 23 # Prime number
    g = 5  # Primitive root modulo p
    
    # Generation of secret number
    private_number_a = os.urandom(16)
    secret_number_b = pow(g, int.from_bytes(private_number_a, "big"), p)
    print("Key generated by :", secret_number_b)
    

    # Generation of signature
    signature = generate_signature(private_key_b)

    
    # Encrypt the message
    encrypted_blocks = encrypt_message(secret_number_b, signature, client_a_public)

    # Receive the message
    decrypted_data = receive_and_decrypt_message(private_key_b,encrypted_blocks)

    # Send the message
    #send_encrypted_message(encrypted_blocks)

    key_generated_from_a = verify_signature(decrypted_data,client_a_public)
    
    
    print("Key generated by B:", key_generated_from_a.decode())
    
    private_key = pow(int(key_generated_from_a.decode()), int.from_bytes(private_number_a, "big"), p)
    
    print("Private key:", private_key)
    
    aes_key = sha256(str(private_key).encode()).digest()

    message = input("Enter the message to send to client A: ")
    iv, ciphertext = encrypt_aes(aes_key, message)
    send_symmetric_message(iv, ciphertext)