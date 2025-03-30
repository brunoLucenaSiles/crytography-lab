import sys

# Alphabets to be used in the encryption and decryption
alphabet_mayus = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alphabet_minus = "abcdefghijklmnopqrstuvwxyz"

# Function to decrypt a message encrypted with the Caesar cipher
def decrypt_caesar(encrypted_message, moves):
    decrypt_message = ""
    for character in encrypted_message:
        if character in alphabet_mayus:
            # Encontrar la posición original restando el desplazamiento
            position = (alphabet_mayus.index(character) - moves) % len(alphabet_mayus)
            decrypt_message += alphabet_mayus[position]
        elif character in alphabet_minus:
            position = (alphabet_minus.index(character) - moves) % len(alphabet_minus)
            decrypt_message += alphabet_minus[position]
        else:
            decrypt_message += character  # Maintain the character if it is not in the alphabet
    return decrypt_message

if __name__ == "__main__":

    if(len(sys.argv) != 3):
        print("Usage: python decryptCaesar.py <file.txt> <moves>")
        sys.exit(1)

    print("Caesar Cipher Decryption")
    file = sys.argv[1]
    moves = int(sys.argv[2])

    try:
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: The file '{file}' doesn't exist.")
        sys.exit(1)

    print(f"Number received: {moves}")
    print(f"Content of the file '{file}':\n{content}")
    decrypted_message = decrypt_caesar(content, moves)
    print(f"Decrypted message: {decrypted_message}")