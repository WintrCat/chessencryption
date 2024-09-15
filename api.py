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
pgn_moves = """
[Event "Bot Match"]
[Site "https://lichess.org"]
[Date "2024.04.27"]
[Round "-"]
[White "Bot1"]
[Black "Bot2"]
[Result "1-0"]

1. d3 c6 2. Bg5 Nh6 3. Bf4 c5 4. Bd2 a6 5. Bg5 f6 6. Bxf6 Qa5+ 7. Bc3 Qb4 8. Bxb4 Ng8 9. Bxc5 Nh6 10. Bxe7 Rg8 11. Bxf8 Rh8 12. Bxg7 a5 13. Be5 Ra6 14. Bc3 Rg8 15. Nh3 Kf8 16. Bd2 Rg4 17. Ng5 Kg8 18. Nxh7 Kh8 19. Nf8 Kg8 20. Qc1 Rgg6 21. Nh7 Kh8 22. Nf8 Kg8 23. Nh7 Kxh7 24. Na3 Nc6 25. Be3 Kh8 26. Bg5 Kg8 27. Bd8 Kh8 28. Be7 Kg8 29. Bc5 Rg3 30. Bf8 Na7 31. Bg7 Rag6 32. f3 Rc6 33. Bh8 Kxh8 34. Nb5 Kg8 35. Nc7 Ra6 36. Kd1 Nc6 37. Ne8 Nf7 38. Qb1 Nh6 39. Rg1 Nf7 40. Kd2 Nd6 41. Nf6+ Kf7 42. Ne8 Rg6 43. Qc1 Rg8 44. d4 Ne5 45. Qe1 Nec4+ 46. Kd3 Rg7 47. a3 Rxg2 48. a4 Nxb2+ 49. Kc3 Rb6 50. Qb1 Ke6 51. Qa2+ Ke7 52. Rh1 Nf5 53. Qb3 Re6 54. Qxb7 Rexe2 55. Ra3 Rg3 56. Qa7 Re4 57. Nf6 Nh4 58. Qc7 Re5 59. Kb3 Re2 60. Ng4 Rh3 61. Qb8 Re5 62. Qxe5+ Kd8 63. Qe8+ Kc7 64. Bd3 Ng2 65. Ba6 Kd6 66. Nf6 Rxh2 67. Kxb2 Bb7 68. Qe6+ Kxe6 69. Kc3 Kxf6 70. Ra2 Rh7 71. Bd3 Be4 72. Rxh7 Bg6 73. Re7 Bxd3 74. Re2 Nf4 75. Rd2 Kf5 76. Rd1 Be4 77. Rf1 Bb7 78. Kb2 Ke6 79. Raa1 Ng6 80. Rfe1+ Kf5 81. Kb1 Bxf3 82. Re2 Kg4 83. Ka2 Kg5 84. Rh1 Ne7 85. Kb1 Bd5 86. Ree1 Nc6 87. Re5+ Kg4 88. Ree1 Be6 89. Rh6 Na7 90. Rexe6 Nc6 91. Re8 Na7 92. Rf8 Kg5 93. Rf3 Kxh6 94. Rf7 Kg5 95. d5 Nc6 96. Rf1 Nd4 97. Kc1 Nc6 98. Kb2 Ne7 99. Rg1+ Kf6 100. Rf1+ Ke5 101. Rf4 Kd6 102. Rf1 Nc8 103. Rf4 Kxd5 104. Re4 Kc5 105. Rd4 Kxd4 106. c3+ Kd5 107. Kc2 Kc6 108. Kb3 Kd6 109. Kc2 Nb6 110. Kd1 Nc8 111. Kd2 Nb6 112. c4 Kc5 113. Kc2 Kd6 114. Kd1 Kc5 115. Kc2 Nxc4 116. Kd3 Kb6 117. Kxc4 Ka7 118. Kb5 Ka8 119. Ka6 Kb8 120. Kb6 d6 121. Ka6 Ka8 122. Kb5 d5 123. Kc6 Ka7 124. Kc7 Ka8 125. Kc8 d4 126. Kd7 Kb8 127. Ke8 Ka8 128. Kd8 d3 129. Ke8 Kb8 130. Kd8 d2 131. Ke7 d1=R 132. Ke8 Rd4 133. Kf7 Rh4 134. Kg7 Rd4 135. Kf7 Kc7 136. Ke8 Kd6 137. Kf8 Kc6 138. Kf7 Kb6 139. Kg6 Rh4 140. Kg5 Ka7 141. Kxh4 Ka8 142. Kg4 Kb7 143. Kh3 Ka7 144. Kg4 Kb7 145. Kf5 Kc7 146. Ke5 Kb8 147. Ke6 Kc8 148. Kf7 Kc7 149. Ke8 Kc8 150. Kf7 Kd7 151. Kg6 Ke7 152. Kh6 Kf7 153. Kh7 Kf6 154. Kg8 Ke6 155. Kg7 Kf5 156. Kg8 Ke5 157. Kg7 Kd5 158. Kh6 Ke6 159. Kg7 Ke7 160. Kh6 Kd7 161. Kh5 Kc7 162. Kh6 Kc8 163. Kg7 Kd8 164. Kf7 Kc8 165. Kf6 Kc7 166. Kg5 Kd6 167. Kh4 Kc5 168. Kh5 Kd6 169. Kh6 Kd5 170. Kg7 Kd4 171. Kg6 Kc3 172. Kh6 Kb4 173. Kh5 Kc3 174. Kh6 Kc4 175. Kh5 Kd4 176. Kh4 Ke3 177. Kg4 Kf2 178. Kh5 Ke2 179. Kg6 Ke3 180. Kf6 Kf2 181. Kg7 Kg3 182. Kg6 Kf2 183. Kg7 Kg2 184. Kf7 Kf3 185. Kf8 Kf4 186. Kg8 Ke3 187. Kf8 Ke2 188. Kf7 Ke3 189. Kg8 Ke2 190. Kg7 Kf2 *
"""

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

    # Monitor the game until it concludes
    monitor_game(client_bot1, accepted_game_id)

if __name__ == "__main__":
    main()
