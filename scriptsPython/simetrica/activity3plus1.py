from collections import Counter
import string
import matplotlib.pyplot as plt
import numpy as np
from activitiy1 import alphabet_minus, alphabet_mayus, decrypt_caesar

def analyze_counts(text):
    # Remove all characters that are not letters
    letters_only = ""
    for char in text:
        if char in alphabet_minus:
            letters_only += char

    return Counter(letters_only)


def analyze_counts(text):
    # Remove all characters that are not letters
    letters_only = ""
    for char in text:
        if char in alphabet_minus:
            letters_only += char

    return Counter(letters_only)


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
    # Read both files texts
    with open("quijote.txt", "r", encoding="utf-8") as file:
        book_text = file.read()

    with open("finis-mundi-encrypted.txt", "r", encoding="utf-8") as file:
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