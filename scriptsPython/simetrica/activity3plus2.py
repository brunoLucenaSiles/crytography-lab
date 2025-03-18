from collections import Counter
import string
import numpy as np
from activity3plus1 import calculate_average_offset
from activitiy1 import decrypt_caesar

# Function to extract the one letter words from a text
def one_letter_words_func(text):
    words = text.lower().split()
    one_letter_words = []
    for word in words:
        if len(word) == 1 and word in string.ascii_lowercase:
            one_letter_words.append(word)    
    
    count = Counter(one_letter_words)
    return count


    offsets = []

    # Compare the frequencies of the most common words
    for (cypher_word, _), (book_word, _) in zip(cypher_counts.most_common(), book_counts.most_common()):

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

    book_counts = one_letter_words_func(book_text)
    print("Book word count:", book_counts)

    cypher_counts = one_letter_words_func(encrypted_text)
    print("Encrypted text word count:", cypher_counts)
    
    average_offset = calculate_average_offset(book_counts, cypher_counts)
    print(f"Calculated average offset: {average_offset}")
    
    decrypted_text = decrypt_caesar(encrypted_text, average_offset)
    print("See the output text:\n")
    
    # Save the decrypted text to a file
    with open("finis-mundi-decrypted.txt", "w", encoding="utf-8") as file:
        file.write(decrypted_text)  
