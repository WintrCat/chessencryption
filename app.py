"""
======================================================
CHESS ENCRYPTION SCRIPT
Author: @Balaji303
Description: 
This script provides encryption and decryption functionalities using chess-based encoding techniques. 
It utilizes external `encode` and `decode` modules for converting files to and from encrypted formats.
======================================================
"""

# Import the required functions for encoding and decoding
from decode import *
from encode import *
# Importing the os module to interact with the operating system (e.g., file handling)
import os  

"""
Initializes the encryption process by taking input from the user for source file and output file.

Returns:
- input_file: Path to the source file to be encrypted.
- output_file_path: Path where the encrypted file will be saved.
"""
def encrypt_init():

    # Prompt the user to input the file path they want to encrypt
    input_file = input("Enter the file path: ")
    
    # Prompt the user to input the desired output file name
    output_file_path = input("Enter the output file name: ")
    
    # Append ".txt" to the output file name as the encryption result will be stored in a text file
    output_file_path += ".txt"
    
    return input_file, output_file_path  # Return the source file path and the output encrypted file path

"""
Performs the encryption process by calling the `encode` function and saving the result.

Args:
- source_file: Path to the file to be encrypted.
- encrypted_file: Path where the encrypted data will be saved.
"""
def encryption(source_file, encrypted_file):

    try:
        # Get the size of the source file for an estimated encryption time
        source_file_size = os.path.getsize(source_file)
        
        # Display an estimated time for encryption based on file size
        print(f"⏳ Estimated time for Encryption {int((source_file_size / 1024) * 2)} seconds")
        
        # Call the encode function to encrypt the source file's data
        encrypted_result = encode(source_file)
        
        # Open the output file in write mode and save the encrypted result
        with open(encrypted_file, "w") as file:
            file.write(encrypted_result)
        
        # Inform the user that encryption was successful
        print(f"🔒 Encrypt successfully saved to {encrypted_file}")
        
    except FileNotFoundError:
        # Handle the case when the source file is not found
        print(f"❌ Error: The file '{source_file}' was not found.")
    except Exception as e:
        # Catch any other exceptions and display the error message
        print(f"❌ An error occurred: {e}")

"""
    Performs the decryption process by calling the `decode` function and saving the result.
    
    Args:
    - encrypted_file: Path to the encrypted file.
    - source_file: Path where the decrypted original file will be saved.
"""
def decryption(encrypted_file, source_file):
    
    try:
        # Open the encrypted file in read mode and load the encrypted PGN string
        with open(encrypted_file, 'r') as f:
            encrypted_string = f.read()
        
        # Call the decode function to decrypt the encrypted data and save it to the original source file
        decode(encrypted_string, source_file)
        
        # Inform the user that decryption was successful
        print(f"🔓 Decoded data has been written to {source_file}")
        
    except FileNotFoundError:
        # Handle the case when the encrypted file is not found
        print(f"❌ Error: File '{encrypted_file}' not found.")
    except Exception as e:
        # Catch any other exceptions and display the error message
        print(f"❌ An error occurred: {e}")

"""
Initializes the decryption process by taking input from the user for encrypted file and output file.

Returns:
- input_file: Path to the encrypted file.
- output_file_path: Path where the decrypted file will be saved.
"""
def decrypt_init():

    # Prompt the user to input the file path of the encrypted file
    input_file = input("Enter the encrypt file path: ")
    
    # Prompt the user to input the desired output file name (including extension)
    output_file_path = input("Enter the output file name ( with extension example- pic.png ): ")
    
    return input_file, output_file_path  # Return the encrypted file path and the output decrypted file path

"""
Main execution block of the script. 
This section runs the encryption followed by the decryption process.
"""
if __name__ == "__main__":
    
    # Initialize encryption by getting the source file and the output file for encryption
    source_file, encrypted_file = encrypt_init()
    
    # Call the encryption function to encrypt the source file
    encryption(source_file, encrypted_file)
    
    # Initialize decryption by getting the encrypted file and the output file for decryption
    encrypted_file, decrypted_original_file = decrypt_init()
    
    # Call the decryption function to decrypt the encrypted file
    decryption(encrypted_file, decrypted_original_file)
