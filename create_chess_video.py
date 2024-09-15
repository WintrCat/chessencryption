import os
import sys
import chess.pgn
import pygame
from pygame.locals import *
import subprocess

# Define constants
WIDTH, HEIGHT = 640, 640  # Window size
SQUARE_SIZE = WIDTH // 8
FPS = 1  # Frames per second (controls move speed)
IMAGE_FOLDER = 'frames'  # Folder to save frames
PIECE_IMAGES = {}  # Dictionary to hold piece images

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Chess Game Replay')
clock = pygame.time.Clock()

def load_piece_images():
    pieces = ['wp', 'wn', 'wb', 'wr', 'wq', 'wk',
              'bp', 'bn', 'bb', 'br', 'bq', 'bk']
    for piece in pieces:
        image = pygame.image.load(os.path.join('images', piece + '.png'))
        PIECE_IMAGES[piece] = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))

def draw_board(screen):
    colors = [pygame.Color(235, 235, 208), pygame.Color(119, 148, 85)]  # Light and dark squares
    for rank in range(8):
        for file in range(8):
            color = colors[(rank + file) % 2]
            rect = pygame.Rect(file*SQUARE_SIZE, rank*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, color, rect)

def draw_pieces(screen, board):
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_color = 'w' if piece.color == chess.WHITE else 'b'
            piece_type = piece.symbol().lower()
            piece_image = PIECE_IMAGES[piece_color + piece_type]
            rank = 7 - chess.square_rank(square)  # Flip the rank to match display orientation
            file = chess.square_file(square)
            screen.blit(piece_image, (file * SQUARE_SIZE, rank * SQUARE_SIZE))
            

def save_frame(frame_number):
    if not os.path.exists(IMAGE_FOLDER):
        os.makedirs(IMAGE_FOLDER)
    filename = os.path.join(IMAGE_FOLDER, f'frame_{frame_number:04d}.png')
    pygame.image.save(screen, filename)

def main():
    if len(sys.argv) < 2:
        print("Usage: python create_chess_video.py <pgn_file>")
        sys.exit(1)

    pgn_file = sys.argv[1]
    pgn = open(pgn_file)
    game = chess.pgn.read_game(pgn)

    board = game.board()
    move_history = list(game.mainline_moves())

    load_piece_images()
    frame_number = 0

    # Initial board position
    draw_board(screen)
    draw_pieces(screen, board)
    pygame.display.flip()
    save_frame(frame_number)
    frame_number += 1

    for move in move_history:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        board.push(move)

        draw_board(screen)
        draw_pieces(screen, board)
        pygame.display.flip()
        save_frame(frame_number)
        frame_number += 1

        clock.tick(FPS)  # Control the speed of the moves

    # After all frames are saved, create the video using ffmpeg
    create_video()

def create_video():
    output_video = 'chess_game.mp4'
    ffmpeg_cmd = [
        'ffmpeg',
        '-framerate', '1',  # Adjust the frame rate as needed
        '-i', os.path.join(IMAGE_FOLDER, 'frame_%04d.png'),
        '-c:v', 'libx264',
        '-r', '30',
        '-pix_fmt', 'yuv420p',
        output_video
    ]
    print("Creating video...")
    subprocess.run(ffmpeg_cmd)
    print(f"Video saved as {output_video}")

if __name__ == '__main__':
    main()
