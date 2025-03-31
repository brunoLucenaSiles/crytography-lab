import sys

# Function to encrypt a message using the Rail Fence cipher
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

if __name__ == "__main__":
    if(len(sys.argv) != 3):
        print("Usage: python encryptRailFence.py <filename.txt> <moves> ")
        sys.exit(1)

    print("Rail Fence Encryption")
    file = sys.argv[1]
    moves = int(sys.argv[2])

    try:
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
            print(f"Message read. The file length is of: {len(content)} bits" )
    except FileNotFoundError:
        print(f"Error: The file '{file}' doesn't exist.")
        sys.exit(1)


    encrypted_message = encrypt_rail_fence(content, moves)
    print(f"Content of the file: {content}")
    print(f"Number of moves: {moves}")
    print("Message encrypted")
    open ("encrypted_messageRailFence.txt", "w").write(encrypted_message)