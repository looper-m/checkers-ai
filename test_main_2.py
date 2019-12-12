import time
import game_pieces

from algorithm import Algorithm
from board import Board
from empty_piece import EmptyPiece
from king_piece import KingPiece
from piece import Piece
from player import Player


def print_board(board_to_print):
    for row in board_to_print.board:
        row_pieces = []
        for piece in row:
            row_pieces.append(piece.symbol)
        print("|" + "|".join(row_pieces) + "|")


RED = Player(True, "RED", game_pieces.RED_PIECE, game_pieces.RED_KING_PIECE)
BLACK = Player(False, "BLACK", game_pieces.BLACK_PIECE, game_pieces.BLACK_KING_PIECE)
board = Board(RED, BLACK)

# random piece placements to test
king = KingPiece(3, 1, BLACK)
board.board[3][1] = king
board.board[4][2] = Piece(4,2, RED)
board.board[6][3] = EmptyPiece()
board.board[6][7] = EmptyPiece()
board.board[7][4] = EmptyPiece()


print_board(board)
print("\n")

possible_king_boards = board.get_possible_boards_for_piece(king)
for possible_board in possible_king_boards:
    print_board(possible_board)
    print("\n")