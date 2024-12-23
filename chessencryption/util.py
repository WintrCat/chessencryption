from chess import pgn
from io import StringIO


def to_binary_string(num: int, bits: int):
    binary = bin(num)[2:]
    binary = ("0" * (bits - len(binary))) + binary

    return binary


def get_pgn_games(pgn_string: str):
    games: list[pgn.Game] = []

    pgn_stream = StringIO(pgn_string)

    while True:
        game = pgn.read_game(pgn_stream)

        if game is None:
            break
        else: 
            games.append(game)

    return games
