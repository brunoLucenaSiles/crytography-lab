alphabet_mayus = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alphabet_minus = "abcdefghijklmnopqrstuvwxyz"


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


def encrypt_rail_fence(message, rails):
    if rails < 2:
        return message  # No encryption for 1 rail
    
    # Create empty rails
    railArray = []
    for i in range(rails):
        railArray.append('')

    row = 0
    step = 1
    
    for char in message:
        railArray[row] += char
        
        # Change direction at top and bottom rails
        if row == 0:
            step = 1
        elif row == rails - 1:
            step = -1
        row += step
    
    # Concatenate all rows to get the cipher text
    return ''.join(railArray)


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


def decrypt_rail_fence(encrypted_message, rails):
    if rails < 2:
        return encrypted_message  # No decryption needed for 1 rail
    
    # Determine the zigzag pattern
    railArray = []
    for i in range(rails):
        railArray.append([''] * len(encrypted_message))

    row = 0
    step = 1
    
    # Mark positions where characters will be placed
    for col in range(len(encrypted_message)):
        railArray[row][col] = '*'
        if row == 0:
            step = 1
        elif row == rails - 1:
            step = -1
        row += step

    # Fill the marked positions with the actual characters
    index = 0
    for r in range(rails):
        for c in range(len(encrypted_message)):
            if railArray[r][c] == '*' and index < len(encrypted_message):
                railArray[r][c] = encrypted_message[index]
                index += 1

    # Read the characters in zigzag order
    row = 0
    step = 1
    decrypt_message = []
    
    for col in range(len(encrypted_message)):
        decrypt_message.append(railArray[row][col])
        if row == 0:
            step = 1
        elif row == rails - 1:
            step = -1
        row += step
    
    return ''.join(decrypt_message)

if __name__ == "__main__":
    # Ask the user for the message and the number of moves
    message = input("Enter the message to be encrypted: ")
    encrypted_message = ""
    encryptionTechnique = int(input("Enter the encryption technique (Caesar (0) or Rail Fence(1)): "))
    if encryptionTechnique == 0:
        moves = int(input("Enter the number of moves (key): "))
        encrypted_message = encrypt_caesar(message, moves)
    else :
        rails = int(input("Enter the number of rails: "))
        encrypted_message = encrypt_rail_fence(message, rails)
        
    # Encrypt the message
    print("Encrypted message:", encrypted_message)

    # Decrypt the message
    decrypted_message = ""
    if encryptionTechnique == 0:
        decrypted_message = decrypt_caesar(encrypted_message, moves)
    else :
        decrypted_message = decrypt_rail_fence(encrypted_message, rails)
    print("Decrypted message:", decrypted_message)


    # Test the decryption with an incorrect number of moves
    uncorrect_decrypted_message = ""
    if encryptionTechnique == 0:
        uncorrect_moves = int(input("Enter the number of moves: "))
        uncorrect_decrypted_message = decrypt_caesar(encrypted_message, uncorrect_moves)
    else :
        uncorrect_rails = int(input("Enter the number of rails: "))
        uncorrect_decrypted_message = decrypt_rail_fence(encrypted_message, uncorrect_rails)
    print("Uncorrect decrypted message:", uncorrect_decrypted_message)

