from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

# hay que instalar el paquete pycryptodome
# pip install pycryptodome

def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096
        # Depending the size of the key, the encryption and decryption will be faster or slower
        # Also, the size of the key will determine the security of the key
        # Besides, the size of the key will determine the size of the encrypted message
    )
    public_key = private_key.public_key()
    return private_key, public_key

def encrypt_message(message, public_key_b):
    chunk_size = 214
    data_to_encrypt = str(message).encode()
    encrypted_blocks = []

    # Divide the message in chunks
    for i in range(0, len(data_to_encrypt), chunk_size):
        chunk = data_to_encrypt[i:i + chunk_size]
            
        # Cypher the chunk
        encrypted_chunk = public_key_b.encrypt(
            chunk,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        encrypted_blocks.append(encrypted_chunk) 
        
    return encrypted_blocks



def decrypt_message(encrypted_blocks, private_key_b):
    decrypted_data = b""
    for encrypted_part in encrypted_blocks:
        decrypted_part = private_key_b.decrypt(
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

if __name__ == "__main__":
    private_key_a, public_key_a = generate_keys()

    private_key_b, public_key_b = generate_keys()

    print("Keys generated")
    message = input("Enter a message to sent to B: ")

    print("Creating signature")
    print("Encrypting message")
    encrypted_blocks = encrypt_message(message, public_key_b)
    print(encrypted_blocks)
    print("Sending message from A to B")

    decrypted_message = decrypt_message(encrypted_blocks, private_key_b)

    print("Decrypted message:", decrypted_message)

