from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

# hay que instalar el paquete pycryptodome
# pip install pycryptodome
def generate_signature(private_key,message):
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

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

def encrypt_message(message, signature, public_key):
    chunk_size = 214
    data_to_encrypt = message + b"||SIGNATURE||" + signature
    encrypted_blocks = []

    # Divide the message in chunks
    for i in range(0, len(data_to_encrypt), chunk_size):
        chunk = data_to_encrypt[i:i + chunk_size]
            
        # Cypher the chunk
        encrypted_chunk = public_key.encrypt(
            chunk,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        encrypted_blocks.append(encrypted_chunk) 
        
    return encrypted_blocks

def verify_signature(decrypted_data, client_public_key):
    message, signature = decrypted_data.split(b"||SIGNATURE||") 

    try:
        client_public_key.verify(
            signature,  # Firma a verificar
            message,    # Mensaje original
            padding.PSS(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH  # Longitud del salt
            ),
            hashes.SHA256()  # Algoritmo hash utilizado
        )
        print("The firm is valid")
        return message.decode()
    except Exception as e:
        print("The firm is not valid:", e)
        return None
        
    

def decrypt_message(encrypted_blocks, private_key):
    decrypted_data = b""
    for encrypted_part in encrypted_blocks:
        decrypted_part = private_key.decrypt(
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
    message = input("Enter a message to sent to B: ").encode()

    print("Creating signature")
    print("Encrypting message")
    signature = generate_signature(private_key_a,message)

    encrypted_blocks = encrypt_message(message, signature,public_key_b)
    print("Sending message from A to B")
    print(encrypted_blocks)

    decrypted_message = decrypt_message(encrypted_blocks, private_key_b)

    messageDecryptedVerified = verify_signature(decrypted_message,public_key_a)

    print("Decrypted message:", messageDecryptedVerified)


