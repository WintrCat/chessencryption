from chess import pgn
from json import load
from io import StringIO
import requests

config = load(open("config.json"))


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


def play_game(game: pgn.Game):
    # get spongebob to send a challenge to patrick
    challenge_request = requests.post(
        f"https://lichess.org/api/challenge/{config["patrick"]["username"]}",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Bearer {config["spongebob"]["token"]}"
        },
        data="color=white"
    )

    challenge_id = challenge_request.json()["id"]
    print(f"challenge sent to patrick with id: {challenge_id}")

    # get patrick to accept the challenge
    accept_challenge_request = requests.post(
        f"https://lichess.org/api/challenge/{challenge_id}/accept",
        headers={
            "Authorization": f"Bearer {config["patrick"]["token"]}"
        }
    )

    print(f"accept challenge request response: {accept_challenge_request.json()}")

    # get the game being played
    game_request = requests.get(
        f"https://lichess.org/api/user/{config["spongebob"]["username"]}/current-game",
        headers={
            "Accept": "application/json"
        }
    )

    game_id: str = game_request.json()["id"]
    print(f"patrick accepted to make game id: {game_id}")

    game_start_time: int = game_request.json()["createdAt"]

    # start playing out the moves in the current pgn game
    game_moves = enumerate(
        list(game.mainline_moves())
    )

    for move_index, move in game_moves:
        player = ["spongebob", "patrick"][move_index % 2]

        requests.post(
            f"https://lichess.org/api/bot/game/{game_id}/move/{move.uci()}",
            headers={
                "Authorization": f"Bearer {config[player]["token"]}"
            }
        )

    # after moves are played, spongebob resigns for next game
    requests.post(
        f"https://lichess.org/api/bot/game/{game_id}/resign",
        headers={
            "Authorization": f"Bearer {config["spongebob"]["token"]}"
        }
    )

    return (game_id, game_start_time)
