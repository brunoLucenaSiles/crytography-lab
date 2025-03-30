import sys

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

    if(len(sys.argv) != 3):
        print("Usage: python decryptRailFence.py <file.txt> <moves>")
        sys.exit(1)


    print("Rail Fence Decryption")
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
    decrypted_message = decrypt_rail_fence(content, moves)
    print(f"Decrypted message: {decrypted_message}")
