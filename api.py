import berserk
import time
import chess.pgn
from io import StringIO
import os
import logging
import threading

# =========================== CONFIGURATION ===========================

# Option 1: Using Environment Variables for API Tokens (Recommended)
BOT1_TOKEN = ''  # Bot1's API Token
BOT2_TOKEN = ''  # Bot2's API Token

# Replace these with your bots' Lichess usernames
BOT1_USERNAME = ''  # Bot1's Lichess Username
BOT2_USERNAME = ''  # Bot2's Lichess Username

# Define the PGN moves to play
pgn_moves = """ """

# =========================== LOGGING SETUP ===========================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("chess_bots.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# =========================== FUNCTIONS ===========================

def initialize_client(token):
    """
    Initialize a Berserk client with the given token.
    """
    try:
        session = berserk.TokenSession(token)
        client = berserk.Client(session=session)
        logger.info("Initialized Berserk client.")
        return client
    except Exception as e:
        logger.error(f"Failed to initialize Berserk client: {e}")
        raise

def parse_pgn(pgn_string):
    """
    Parse the PGN string and return a list of moves in UCI format.
    """
    try:
        pgn = StringIO(pgn_string)
        game = chess.pgn.read_game(pgn)
        moves = [move.uci() for move in game.mainline_moves()]
        logger.info(f"Parsed PGN with {len(moves)} moves.")
        return moves
    except Exception as e:
        logger.error(f"Failed to parse PGN: {e}")
        raise

def create_challenge(client, opponent_username, color='white', clock_limit=300, clock_increment=5):
    """
    Bot1 challenges Bot2 to a game.
    """
    try:
        challenge = client.challenges.create(
            opponent_username,    # Positional argument
            color=color,
            clock_limit=clock_limit,         # Total time in seconds
            clock_increment=clock_increment, # Increment in seconds per move
            variant='standard',
            rated=True  # Rated game
        )
        game_id = challenge['id']
        logger.info(f"Challenge created with ID: {game_id}")
        return game_id
    except berserk.exceptions.ResponseError as e:
        logger.error(f"Error creating challenge: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error creating challenge: {e}")
        return None

def accept_challenge(client):
    """
    Bot2 listens for incoming challenges and accepts the first one.
    Returns the game ID of the accepted challenge.
    """
    try:
        for event in client.bots.stream_incoming_events():
            if event['type'] == 'challenge':
                challenge = event['challenge']
                challenge_id = challenge['id']
                logger.info(f"Incoming challenge detected with ID: {challenge_id}")
                client.challenges.accept(challenge_id)
                logger.info(f"Accepted challenge ID: {challenge_id}")
                # Retrieve game ID after accepting challenge
                for game_event in client.bots.stream_game_state(challenge_id):
                    if game_event['type'] == 'gameFull':
                        game_id = game_event['id']
                        logger.info(f"Game started with ID: {game_id}")
                        return game_id
    except berserk.exceptions.ResponseError as e:
        logger.error(f"Error accepting challenge: {e}")
    except Exception as e:
        logger.error(f"Unexpected error accepting challenge: {e}")
    return None

def make_move(client, game_id, move):
    """
    Make a move in the specified game using the given client.
    """
    try:
        client.bots.make_move(game_id, move)
        logger.info(f"Move {move} played.")
    except berserk.exceptions.ResponseError as e:
        logger.error(f"Error making move {move}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error making move {move}: {e}")

def resign_game(client, game_id):
    """
    Resign the game using the specified client.
    """
    try:
        client.bots.resign_game(game_id)
        logger.info(f"Resigned game ID: {game_id}")
    except berserk.exceptions.ResponseError as e:
        logger.error(f"Error resigning game {game_id}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error resigning game {game_id}: {e}")

def create_game_link(game_id):
    """
    Create a Lichess game link from the game ID.
    """
    return f"https://lichess.org/{game_id}"

def parse_game_result(client, game_id):
    """
    Retrieve and return the game's result.
    """
    try:
        game = client.games.export_by_id(game_id)
        return game.get('winner', 'draw')
    except Exception as e:
        logger.error(f"Error retrieving game result for {game_id}: {e}")
        return "Unknown"

def create_pgn_from_game(client, game_id):
    """
    Export the PGN of the completed game.
    """
    try:
        pgn = client.games.export_pgn(game_id)
        return pgn
    except Exception as e:
        logger.error(f"Error exporting PGN for game {game_id}: {e}")
        return ""

def play_game(client_bot1, client_bot2, game_id, moves):
    """
    Play through the predefined moves in the game.
    """
    board = chess.Board()
    for idx, move in enumerate(moves):
        if board.is_game_over():
            logger.info("Game is already over.")
            break

        if board.turn == chess.WHITE:
            # It's White's turn - Bot1
            current_client = client_bot1
            current_bot = BOT1_USERNAME
            logger.info(f"Turn {idx + 1}: {current_bot} to play {move}")
            make_move(current_client, game_id, move)
        else:
            # It's Black's turn - Bot2
            current_client = client_bot2
            current_bot = BOT2_USERNAME
            logger.info(f"Turn {idx + 1}: {current_bot} to play {move}")
            make_move(current_client, game_id, move)

        try:
            board.push_uci(move)
        except ValueError as e:
            logger.error(f"Invalid move '{move}': {e}")
            break
        time.sleep(1)  # Optional: Add delay between moves to comply with API rate limits

    logger.info("Finished playing all predefined moves.")

def monitor_game(client, game_id):
    """
    Monitor the game status until it concludes.
    """
    try:
        for event in client.bots.stream_game_state(game_id):
            status = event.get('status')
            if status in ['mate', 'resign', 'timeout', 'draw', 'stalemate', 'adjudication']:
                logger.info(f"Game ended with status: {status}")
                break
            time.sleep(1)
    except berserk.exceptions.ConnectionError:
        logger.error("Connection lost while monitoring the game.")
    except Exception as e:
        logger.error(f"An error occurred while monitoring the game: {e}")

def listen_and_accept(client_bot2, game_id_container):
    """
    Thread function for Bot2 to accept challenge.
    """
    accepted_game_id = accept_challenge(client_bot2)
    if accepted_game_id:
        game_id_container.append(accepted_game_id)

# =========================== MAIN SCRIPT ===========================

def main():
    # Initialize clients for both bots
    client_bot1 = initialize_client(BOT1_TOKEN)
    client_bot2 = initialize_client(BOT2_TOKEN)

    # Parse PGN to get the list of moves
    try:
        moves = parse_pgn(pgn_moves)
        logger.info(f"Total moves to play: {len(moves)}")
    except Exception:
        logger.critical("Failed to parse PGN. Exiting.")
        return

    # Container to hold the accepted game ID
    game_id_container = []

    # Start a thread for Bot2 to listen and accept the challenge
    listener_thread = threading.Thread(target=listen_and_accept, args=(client_bot2, game_id_container))
    listener_thread.start()

    # Bot1 creates a challenge to Bot2
    game_id = create_challenge(client_bot1, BOT2_USERNAME, color='white')
    if not game_id:
        logger.critical("Failed to create a challenge. Exiting.")
        return

    # Wait for Bot2 to accept the challenge
    listener_thread.join(timeout=30)  # Wait up to 30 seconds
    if not game_id_container:
        logger.critical("Bot2 did not accept the challenge in time. Exiting.")
        return

    accepted_game_id = game_id_container[0]
    logger.info(f"Game started with ID: {accepted_game_id}")

    # Play through the moves
    play_game(client_bot1, client_bot2, accepted_game_id, moves)

    # Resign the game after all moves are played
    # Decide which bot should resign. For this example, we'll have Bot2 resign.
    resign_game(client_bot2, accepted_game_id)

    # Generate and log the game link
    game_link = create_game_link(accepted_game_id)
    logger.info(f"Game Link: {game_link}")

    # Optionally, you can export and log the PGN of the completed game
    pgn = create_pgn_from_game(client_bot1, accepted_game_id)
    if pgn:
        with open(f"{accepted_game_id}.pgn", "w") as pgn_file:
            pgn_file.write(pgn)
        logger.info(f"PGN of the game has been saved to {accepted_game_id}.pgn")

    # Monitor the game until it concludes
    monitor_game(client_bot1, accepted_game_id)

if __name__ == "__main__":
    main()
