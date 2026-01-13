import argparse
import sys
import os
from encode import encode
from decode import decode

def main():
    parser = argparse.ArgumentParser(description="Chess Encryption: Hide files in PGN games.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    encode_parser = subparsers.add_parser("encode", help="Encrypt a file into PGN format")
    encode_parser.add_argument("input", help="Path to the file you want to encrypt")
    encode_parser.add_argument("output", help="Path where the PGN will be saved")

    decode_parser = subparsers.add_parser("decode", help="Decrypt a PGN file back to original")
    decode_parser.add_argument("input", help="Path to the PGN file")
    decode_parser.add_argument("output", help="Path where the decoded file will be saved")

    args = parser.parse_args()

    if args.command == "encode":
        if not os.path.exists(args.input):
            print(f"Error: Input file '{args.input}' does not exist.")
            return

        print(f"Encrypting {args.input} -> {args.output}")
        pgn_data = encode(args.input)
        
        with open(args.output, "w") as f:
            f.write(pgn_data)
        print("Done.")

    elif args.command == "decode":
        if not os.path.exists(args.input):
            print(f"Error: Input PGN '{args.input}' does not exist.")
            return

        print(f"Decrypting {args.input} -> {args.output}")
        
        with open(args.input, "r") as f:
            pgn_content = f.read()
            
        decode(pgn_content, args.output)
        print("Done.")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()