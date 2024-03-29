#Download python newest release, Set up your BASE_DIR before running the code.
#This should be used To safely store passwords on computers or other TXT data
#This is NOT fully safe as when bad Actors can see the Code they could decode it so rename this file to something ordinary like "unusedproject"
#Made by Rudy_Dev
BASE_DIR = r"C:\Users"
Version = "v1" #don't change this, it's a indicator of your version

import os
import base64
import secrets
import uuid

def caesar_cipher(text, shift=4, decode=False):
    """
    Apply Caesar cipher to the given text.
    If decode is True, it will decode the text.
    """
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    table = str.maketrans(alphabet, shifted_alphabet) if not decode else str.maketrans(shifted_alphabet, alphabet)
    return text.translate(table)

def generate_guid_file():
    filename = input("Enter the file name for the GUID: ")
    # Ensure the filename has a .txt extension
    if not filename.endswith('.txt'):
        filename += '.txt'
    file_path = os.path.join(BASE_DIR, filename)
    file_path = os.path.join(BASE_DIR, filename)

    print("Choose the number of UUIDs to generate:")
    choice = input("S for 1 UUID, D for 2 UUID's or F for 4 UUID's: ").upper()

    if choice == 'S':
        guid = uuid.uuid4()
        with open(file_path, 'w') as file:
            file.write(str(guid))
        print(f"1 UUID generated and saved to {filename}")
    elif choice == 'D':
        guid1 = uuid.uuid4()
        guid2 = uuid.uuid4()
        merged_guid = f"{guid1}-{guid2}"
        with open(file_path, 'w') as file:
            file.write(merged_guid)
        print(f"2 UUIDs generated and merged, saved to {filename}")
    elif choice == 'F':
        guid1 = uuid.uuid4()
        guid2 = uuid.uuid4()
        guid3 = uuid.uuid4()
        guid4 = uuid.uuid4()
        merged_guid = f"{guid1}-{guid2}-{guid3}-{guid4}"
        with open(file_path, 'w') as file:
            file.write(merged_guid)
        print(f"4 UUIDs generated and merged, saved to {filename}")
    else:
        print("Invalid choice. Please choose S for 1 UUID or D for 2 UUIDs.")

def main():
    print("welcome to General Text Encrypt Software, also known as GTES")
    print("This Is",Version,"Of General TXT encoder mady by Rudy_Dev")
    print("This is first release,if you encounter any bugs please contact Rudy")
    print("your Base Directory is Set to",BASE_DIR)
    print("if this isn't Directory you want to edit open the file with text editor and Edit it")
    while True:
        print("Choose Encoding or Decoding")
        choice = input("E for Encoding, D for Decoding, R for Reset, G to Generate a Safe Password(GUID): ").upper()
       
        if choice == 'E':
            try:
                encode_file()
            except Exception as e:
                print(f"An error occurred: {e}")
                print("Resetting...")
                continue
        elif choice == 'D':
            try:
                decode_file()
            except Exception as e:
                print(f"An error occurred: {e}")
                print("Resetting...")
                continue
        elif choice == 'R':
            print("Resetting...")
            continue
        elif choice == 'G':
            generate_guid_file()
            continue
        else:
            print("Invalid choice. Please choose E for Encoding, D for Decoding, R for Reset, or G for Generate GUID.")

def encode_file():
    # List all files in the BASE_DIR
    files = [file for file in os.listdir(BASE_DIR) if not file.startswith("e_")]
    print("Available files for encoding:")
    for index, file in enumerate(files, start=1):
        print(f"{index}. {file}")
    
    filename = input("Enter the file name to encode: ")
    if not filename.startswith("e_"):
            # Proceed with the encoding process
        file_path = os.path.join(BASE_DIR, filename)
        if not os.path.isfile(file_path):
            print("File not found.")
            return
    
        with open(file_path, 'rb') as file:
            data = file.read()

        # Encode the data to Base64
        base64_data = base64.b64encode(data)
    
        # Apply Caesar cipher to the Base64-encoded data
        caesar_ciphered_data = caesar_cipher(base64_data.decode('utf-8'), shift=4).encode('utf-8')
    
        # Convert Caesar-ciphered data to binary
        binary_data = ''.join(format(byte, '08b') for byte in caesar_ciphered_data)

        # Generate a unique salt
        salt = secrets.token_bytes(1048)
        # Combine the salt and binary data
        salted_binary_data = salt + binary_data.encode()
        
        encoded_filename = f"e_{filename}"
        encoded_file_path = os.path.join(BASE_DIR, encoded_filename)
        with open(encoded_file_path, 'wb') as file:
            file.write(salted_binary_data)
        print(f"File encoded successfully. New file: {encoded_filename}")

def decode_file():
    # List all files in the BASE_DIR that start with 'e_'
    files = [file for file in os.listdir(BASE_DIR) if file.startswith("e_")]
    if not files:
        print("No encoded files found.")
        return
    print("Encoded files available for decoding:")
    for index, file in enumerate(files, start=1):
        print(f"{index}. {file}")
    
    filename = input("Enter the file name to decode: ")
    file_path = os.path.join(BASE_DIR, filename)
    if not os.path.isfile(file_path):
        print("File not found.")
        return

    # Read the stored salt and binary data
    with open(file_path, 'rb') as file:
        stored_data = file.read()

    # Extract the salt and binary data
    salt = stored_data[:1048] # Assuming the salt is 16 bytes long
    binary_data = stored_data[1048:]

    # Convert binary data back to Caesar-ciphered text
    # Ensure the binary data is correctly formatted as binary
    try:
        caesar_ciphered_data = bytearray(int(binary_data[i:i+8], 2) for i in range(0, len(binary_data), 8))
    except ValueError as e:
        print(f"An error occurred while converting binary data: {e}")
        return

    # Apply Caesar cipher to decode the text
    decoded_base64_data = caesar_cipher(caesar_ciphered_data.decode('utf-8'), shift=4, decode=True).encode('utf-8')

    # Decode the Base64 content
    decoded_data = base64.b64decode(decoded_base64_data)

    decoded_filename = "d_" + filename.replace("e_", "", 1)

    decoded_file_path = os.path.join(BASE_DIR, decoded_filename)
    with open(decoded_file_path, 'wb') as file:
        file.write(decoded_data)
    print(f"File decoded successfully. New file: {decoded_filename}")

if __name__ == "__main__":
    main()
