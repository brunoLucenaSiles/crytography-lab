from collections import Counter
import string
import matplotlib.pyplot as plt
import numpy as np
import sys
alphabet_mayus = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alphabet_minus = "abcdefghijklmnopqrstuvwxyz"

# Function to calculate the frequency of each letter in a text
def calculate_frequencies(text):
    text = text.lower()

    # Remove all characters that are not letters
    letters_only = ""
    for char in text:
        if char in alphabet_minus or char in alphabet_mayus:
            letters_only += char

    total_letters = len(letters_only)
    count = Counter(letters_only)
    frequencies = {}

    # Calculate the frequency of each letter in the text
    for letter in string.ascii_lowercase:
        if total_letters > 0:
            frequencies[letter] = (count[letter] / total_letters) * 100
        else:
            frequencies[letter] = 0
    return frequencies

# Function to plot the letter frequency comparison
def printPlot(book_frequencies, encrypted_frequencies):
    # Prepare the data to be plotted
    letters = list(book_frequencies.keys())
    book_values = list(book_frequencies.values())
    encrypted_values = list(encrypted_frequencies.values())

    # Position of the bars
    x = np.arange(len(letters))
    width = 0.4  # Ancho de las barras

    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 6))

    # Add the bars
    ax.bar(x - width/2, book_values, width, label='Original text', color='skyblue')
    ax.bar(x + width/2, encrypted_values, width, label='Cypher text', color='salmon')

    # Text labels, title and legend
    ax.set_xlabel('Letters', fontsize=12)
    ax.set_ylabel('Frequency (%)', fontsize=12)
    ax.set_title('Letter frequency comparison', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(letters, fontsize=10)
    ax.legend(fontsize=12)

    # Show the plot
    plt.tight_layout()
    plt.show()


# Function to decrypt the text using the mapping
def decripting_with_mapping(text, mapping):
    decrypted_message = ""
    for character in text:
        if character.lower() in mapping:
            new_letter = mapping[character.lower()]
            # Maintain the capitalization of the letter
            decrypted_message += new_letter.upper() if character.isupper() else new_letter
        else:
            decrypted_message += character
    return decrypted_message


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
        
    # Calculate the frequencies of the letters in both texts
    book_frequencies = calculate_frequencies(book_text)
    print("Book percentages (in percentages):", book_frequencies)

    encrypted_frequencies = calculate_frequencies(encrypted_text)
    print("Frequencies of the encrypted text (in percentages):", encrypted_frequencies)
    
    printPlot(book_frequencies, encrypted_frequencies)
    
    
    # Sort the frequencies in descending order to compare them
    sort_book = sorted(book_frequencies, key=book_frequencies.get, reverse=True)
    sort_encrypted = sorted(encrypted_frequencies, key=encrypted_frequencies.get, reverse=True)

    # Create a mapping between the encrypted text and the book text
    # zip(): Create a tuple with the elements of both lists
    mapping = {}
    for encrypted_letter, book_letter in zip(sort_encrypted, sort_book):
        mapping[encrypted_letter[0]] = book_letter[0]
    print("Substitution mapping:", mapping)
    
    # Apply the mapping to decrypt the text
    decrypted_text = decripting_with_mapping(encrypted_text, mapping)
    # print("Decrypted text:\n", decrypted_text)
    
    # Save the decrypted text to a file
    with open("finis-mundi-decrypted.txt", "w", encoding="utf-8") as file:
        file.write(decrypted_text)  