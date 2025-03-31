import nltk
from nltk.corpus import words
import sys

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

# Function to verify the number of valid words in the message
def count_words_valid(text, english_words):     
    words_encrypted = text.split()
    valid_word_count = 0
    for word in words_encrypted:
        if word.lower() in english_words:
            
            valid_word_count += 1
    
    return valid_word_count

if __name__ == "__main__":

    if(len(sys.argv) != 2):
        print("Usage: python BFA_Caesar.py <filename.txt>")
        sys.exit(1)

    filename = sys.argv[1]
    
    nltk.download('words')
    english_words = set(words.words())

    
    # Read the file text - encrypted_caesar_text.txt
    with open(filename, "r") as file:
        encrypted_message = file.read().strip()

    # Variables to store the best decryption
    best_movement = None
    max_valid_words = 0

    # Brute-force attack to decrypt without knowing the key
    print("\nTesting all the possible keys to do a brute-force attack:")
    for move in range(1, len(alphabet_mayus)):
        test_message = decrypt_caesar(encrypted_message, move)
        valid_words = count_words_valid(test_message,english_words)

        print(f"Key {move}: (Number of word valids: {valid_words})")

        if valid_words > max_valid_words:
            print("New best key found")
            max_valid_words = valid_words
            best_movement = move
                
                
    # Show the best decryption
    if best_movement:
        decrypted_message = decrypt_caesar(encrypted_message, best_movement)
        print(f"\nBest key: {best_movement}")
        print("Decrypted message:", decrypted_message)
    else:
        print("It was not found a fine movement.")