# 🔑 Chess Encryption

Encrypt files into large sets of Chess games stored in PGN format.<br>
From the YouTube video: [Storing Files in Chess Games for Free Cloud Storage](https://youtu.be/TUtafoC4-7k?feature=shared)

This is a library so you will need to import functions from `decode.py` and `encode.py` to use this. I have written some small documentation to help using them, although I won't generally be providing support for this software. I'm just uploading it for others with an interest in the algorithm etc.


## CLI Usage

While primarily a library, you may also use this as a CLI for convenience. (If you only intend to use the library, you can safely delete `cli.py`). First, install the required dependency: `pip install -r requirements.txt`

You can now use the CLI to encrypt and decrypt files:
- Encrypt a file
`python cli.py encode input_file.ext output.pgn`

- Decrypt a file
`python cli.py decode output.pgn recovered_file.ext`