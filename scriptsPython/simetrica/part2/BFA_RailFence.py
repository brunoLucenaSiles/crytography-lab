import nltk
from nltk.corpus import words
from part1.decryptRailFence import decrypt_rail_fence
import sys

# Function to verify the number of valid words in the message
def count_words_valid(text, english_words):     
    words_encrypted = text.split()
    valid_word_count = 0
    for word in words_encrypted:
        if word.lower() in english_words:
            
            valid_word_count += 1
    
    return valid_word_count

if __name__ == "__main__":
    nltk.download('words')
    english_words = set(words.words())

    if(len(sys.argv) != 2):
        print("Usage: python BFA_RailFence.py <moves>")
        sys.exit(1)

    print("Rail Fence Brute Force Attack")
    tries = sys.argv[1]
    
    # Read the file text
    with open("encrypted_rail_fence_text.txt", "r") as file:
        encrypted_message = file.read().strip()


    # Variables to store the best decryption
    best_movement = None
    max_valid_words = 0
    move = 0
        
    # Bruteforce attack to decrypt without knowing the key
    print("\nTesting all the possible keys to do a brute-force attack:")
    while move < tries:
        test_message = decrypt_rail_fence(encrypted_message, move)
        valid_words = count_words_valid(test_message,english_words)

        print(f"Movement {move}: (Number of word valids: {valid_words})")

        if valid_words > max_valid_words:
            max_valid_words = valid_words
            best_movement = move
                
        move += 1
                
                
    # Show the best decryption
    if best_movement:
        decrypted_message = decrypt_rail_fence(encrypted_message, best_movement)
        print(f"\nBest movement: {best_movement}")
        print("Decrypted message:", decrypted_message)
    else:
        print("It was not found a fine movement.")