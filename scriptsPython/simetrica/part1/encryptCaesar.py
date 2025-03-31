import sys

# Alphabets to be used in the encryption and decryption
alphabet_mayus = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alphabet_minus = "abcdefghijklmnopqrstuvwxyz"

# Function to encrypt a message using the Caesar cipher
def encrypt_caesar(message, moves):
    encrypt_message = ""
    for character in message.upper():
        if character in alphabet_mayus:
            # Find the position of the character in the alphabet
            position = (alphabet_mayus.index(character) + moves) % len(alphabet_mayus)
            encrypt_message += alphabet_mayus[position]

        elif character in alphabet_minus:
            position = (alphabet_minus.index(character) + moves) % len(alphabet_minus)
            encrypt_message += alphabet_minus[position]

        else:
            encrypt_message += character  # Maintain the character if it is not in the alphabet
    return encrypt_message


if __name__ == "__main__":

    if(len(sys.argv) != 3):
        print("Usage: python encryptCaesar.py <filename.txt> <moves>")
        sys.exit(1)

    print("Caesar Cipher Encryption")
    file = sys.argv[1]
    moves = int(sys.argv[2])

    try:
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
            print(f"Message read. The file length is of: {len(content)} bits" )
    except FileNotFoundError:
        print(f"Error: The file '{file}' doesn't exist.")
        sys.exit(1)

    encrypted_message = encrypt_caesar(content, moves)
    print(f"Content of the file: {content}")
    print(f"Number of moves: {moves}")
    print("Message encrypted")
    open ("encrypted_messageCaesar.txt", "w").write(encrypted_message)