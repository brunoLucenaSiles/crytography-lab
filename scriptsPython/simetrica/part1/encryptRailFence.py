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
        print("Usage: python encryptRailFence.py <message> <moves>")
        sys.exit(1)

    print("Rail Fence Encryption")
    message = sys.argv[1]
    moves = int(sys.argv[2])
    encrypted_message = encrypt_rail_fence(message, moves)
    print(f"Original message: {message}")
    print(f"Number of moves: {moves}")
    print(f"Encrypted message: {encrypted_message}")

    open ("encrypted_messageRailFence.txt", "w").write(encrypted_message)