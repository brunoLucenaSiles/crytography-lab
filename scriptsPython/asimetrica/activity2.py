import hashlib
import sys

def verificate_hash_messages(message1, message2):
    message1 = hashlib.md5(message1.encode())
    print(message1.hexdigest())

    message2 = hashlib.md5(message2.encode())
    print(message2.hexdigest())

    if(message1.digest() == message2.digest()):
        print("The messages are the same")
    else:
        print("The messages are different")

def verificate_hash_files(file1, file2):    
    with open(file1, "rb") as file:
        message1 = hashlib.md5(file.read())
        print(message1.hexdigest())

    with open(file2, "rb") as file:
        message2 = hashlib.md5(file.read())
        print(message2.hexdigest())


    if(message1.digest() == message2.digest()):
        print(f"The {file1} and {file2} are the same")
    else:
        print(f"The {file1} and {file2} are different")

if __name__ == "__main__":
    if(len(sys.argv) != 4):
        print("Usage: python activity2.py <functionName> <wordORfilename1> <wordORfilename2>")
        sys.exit(1)

    functionName = sys.argv[1]
    wordORfilename1 = sys.argv[2]
    wordORfilename2 = sys.argv[3]

    if functionName == "message":
        verificate_hash_messages(wordORfilename1, wordORfilename2)
    elif functionName == "file":
        verificate_hash_files(wordORfilename1, wordORfilename2)
    else:
        print("Invalid option")
        sys.exit(1)