# Project Files

## `bot-upgrade.py`

This script allows you to upgrade a regular Lichess account into a bot account. The `upgrade_to_bot_account` function sends a POST request to the Lichess API to convert the account to a bot.

- **Functions**:
  - `upgrade_to_bot_account(api_token: str)`: Upgrades a Lichess account to a bot account using the provided API token.

[Source file: bot-upgrade.py](file-i7dVakftXvbMHjgMXv5ilGvT)

---

## `create_chess_video.py`

This script generates a video replay of a chess game based on a PGN file. It uses Pygame to create frames of the chessboard, saving each as an image, and then uses `ffmpeg` to compile these images into a video.

- **Features**:
  - Visualize a chess game from PGN and save each frame as an image.
  - Compile saved images into an MP4 video using `ffmpeg`.

[Source file: create_chess_video.py](file-QNHOOYxqv1D5nqlIvyTS1BnF)

---

## `decode.py`

This script decodes a file that has been encoded into PGN-formatted chess games. The `decode` function reads a PGN string, decodes the binary data from chess moves, and reconstructs the original file.

- **Functions**:
  - `decode(pgn_string: str, output_file_path: str)`: Decodes a file from a PGN string and writes it to the output file path.
  - `run_decoder()`: CLI interface for decoding PGN games to files.

[Source file: decode.py](file-amS6fLQMJbsqCWFlk9ZJYIRI)

---

## `encode.py`

This script encodes a file into a series of chess games stored in PGN format. It reads the binary data from a file, converts it into chess moves, and stores the moves as PGN games.

- **Functions**:
  - `encode(file_path: str)`: Encodes a file into chess games in PGN format.
  - `run_encoder()`: CLI interface for encoding files to PGN format.

[Source file: encode.py](file-dBxftbIY2uL2EICCwaS89Zqt)

---

## `api.py`

This script automates chess matches between two Lichess bot accounts. It includes functions for challenging a bot, accepting a challenge, and playing a sequence of predefined PGN moves between two bots.

- **Features**:
  - Automates bot-to-bot chess matches.
  - Uses the Lichess API to create and accept challenges.
  - Executes predefined PGN moves.

[Source file: api.py](file-xnWjzmPTCp6E9I1EsTodqnPe)

---

## Special Thanks

Special thanks to the YouTube video [Storing Files in Chess Games for Free Cloud Storage](https://youtu.be/TUtafoC4-7k?feature=shared) for the inspiration and concept behind this project. This project builds upon ideas introduced in the video, applying them to create a practical implementation for file encryption using chess games.

Additional thanks to:
- **wintrcat**
- [SCP-5370](https://scp-wiki.wikidot.com/scp-5370)

---
