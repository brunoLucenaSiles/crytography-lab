from collections import Counter
import string
import matplotlib.pyplot as plt
import numpy as np
import sys
alphabet_mayus = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alphabet_minus = "abcdefghijklmnopqrstuvwxyz"

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

# Function to extract the one letter words from a text
def analyze_counts(text):
    # Remove all characters that are not letters
    letters_only = ""
    for char in text:
        if char in alphabet_minus:
            letters_only += char

    return Counter(letters_only)

# Function to calculate the number of valid words in the message
def analyze_counts(text):
    # Remove all characters that are not letters
    letters_only = ""
    for char in text:
        if char in alphabet_minus:
            letters_only += char

    return Counter(letters_only)


# Function to calculate the average offset between the most common words
def calculate_average_offset(book_counts, cypher_counts):
    offsets = []

    common_cypher_words  = cypher_counts.most_common()
    common_book_words  = book_counts.most_common()
    
    # Compare the frequencies of the most common words
    for i in range(min(len(common_cypher_words), len(common_book_words))):
        cypher_word = common_cypher_words[i][0]
        book_word = common_book_words[i][0]

        if cypher_word in alphabet_mayus and book_word in alphabet_mayus:
            alphabet = alphabet_mayus
        else:
            alphabet = alphabet_minus

        cypher_index = alphabet.index(cypher_word)
        book_index = alphabet.index(book_word)
        
        print(f"Offset {cypher_word} -> {book_word}: {cypher_index, book_index} ,{(cypher_index - book_index) % len(alphabet_mayus)}")
        offset = (cypher_index - book_index) % len(alphabet_mayus)
        offsets.append(offset)
        
    # Calculate the average offset
    if offsets:
        average = sum(offsets) / len(offsets)
        return round(average)
    return 0


if __name__ == "__main__":
    if(len(sys.argv) != 3):
        print("Usage: python activity3.py <filenameNotDecrypted.txt> <filenameDecrypted.txt>")
        sys.exit(1)

    filenameNotDecrypted = sys.argv[1]
    filenameDecrypted = sys.argv[2]

    # Read both files texts -- quijote.txt and finis-mundi-encrypted.txt
    with open(filenameNotDecrypted, "r", encoding="utf-8") as file:
        book_text = file.read()

    with open(filenameDecrypted, "r", encoding="utf-8") as file:
        encrypted_text = file.read()
        
    book_counts = analyze_counts(book_text)
    cypher_counts = analyze_counts(encrypted_text)

    print("Book frequencies:", book_counts)
    print("Cypher frequencies:", cypher_counts)

    average_offset = calculate_average_offset(book_counts, cypher_counts)
    print(f"Calculated average offset: {average_offset}")

    decrypted_text = decrypt_caesar(encrypted_text, average_offset)
    print("See the output text:\n")
    
    # Save the decrypted text to a file
    with open("finis-mundi-decrypted.txt", "w", encoding="utf-8") as file:
        file.write(decrypted_text)  