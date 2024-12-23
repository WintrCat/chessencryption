import chessencryption
import os

###
### This file will be run by
### GitHub actions to test if the
### program is working correctly.
###

testing_string = "BUY GOLD!"

try:
    os.mkdir("temp")
    print("new directory /temp has been created")
except FileExistsError:
    print("directory /temp already exists")

with open("temp/text.txt", "w") as text_file:
    text_file.write(testing_string)
    print("text.txt has been written")
    text_file.close()

encoded_pgn = chessencryption.encode(file_path="temp/text.txt")

if (encoded_pgn == None):
    print("ERROR: encoded pgn file is empty")
    raise ValueError

chessencryption.decode(pgn_string=encoded_pgn, output_file_path="temp/decoded.txt")

decoded_file = open("temp/decoded.txt", "r")
decoded_text = decoded_file.read()
decoded_file.close()

print("\nOriginal:", testing_string)
print("Decoded:", decoded_text)

if (decoded_text == None):
    print("\nERROR: error when decoding pgn\n")
    raise ValueError

if (decoded_text != testing_string):
    print("\nERROR: values don't match, encryption failed\n")
    raise ValueError

print("\nSUCCESS: values match accordingly")