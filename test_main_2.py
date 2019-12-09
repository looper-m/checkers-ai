import time
import game_pieces

from MTDf import MTDf
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
board.board[0][0] = EmptyPiece()
board.board[0][1] = EmptyPiece()
board.board[0][2] = EmptyPiece()
board.board[0][3] = EmptyPiece()
board.board[0][4] = EmptyPiece()
board.board[0][5] = EmptyPiece()
board.board[0][6] = EmptyPiece()
board.board[0][7] = EmptyPiece()


board.board[1][0] = Piece(1, 0, BLACK)
board.board[1][1] = EmptyPiece()
board.board[1][2] = Piece(1, 2, BLACK)
board.board[1][3] = EmptyPiece()
board.board[1][4] = EmptyPiece()
board.board[1][5] = EmptyPiece()
board.board[1][6] = EmptyPiece()
board.board[1][7] = EmptyPiece()

board.board[2][0] = EmptyPiece()
board.board[2][1] = Piece(2, 1, BLACK)
board.board[2][2] = EmptyPiece()
board.board[2][3] = Piece(2, 3, BLACK)
board.board[2][4] = EmptyPiece()
board.board[2][5] = EmptyPiece()
board.board[2][6] = EmptyPiece()
board.board[2][7] = EmptyPiece()

board.board[3][0] = Piece(3, 0, RED)
board.board[3][1] = EmptyPiece()
board.board[3][2] = Piece(3, 2, BLACK)
board.board[3][3] = EmptyPiece()
board.board[3][4] = EmptyPiece()
board.board[3][5] = EmptyPiece()
board.board[3][6] = KingPiece(3, 6, BLACK)
board.board[3][7] = EmptyPiece()

board.board[4][0] = EmptyPiece()
board.board[4][1] = Piece(4, 1, RED)
board.board[4][2] = EmptyPiece()
board.board[4][3] = EmptyPiece()
board.board[4][4] = EmptyPiece()
board.board[4][5] = EmptyPiece()
board.board[4][6] = EmptyPiece()
board.board[4][7] = EmptyPiece()

board.board[5][0] = Piece(5, 0, RED)
board.board[5][1] = EmptyPiece()
board.board[5][2] = KingPiece(5, 2, BLACK)
board.board[5][3] = EmptyPiece()
board.board[5][4] = EmptyPiece()
board.board[5][5] = EmptyPiece()
board.board[5][6] = EmptyPiece()
board.board[5][7] = EmptyPiece()

board.board[6][0] = EmptyPiece()
board.board[6][1] = EmptyPiece()
board.board[6][2] = EmptyPiece()
board.board[6][3] = KingPiece(6, 3, BLACK)
board.board[6][4] = EmptyPiece()
board.board[6][5] = EmptyPiece()
board.board[6][6] = EmptyPiece()
board.board[6][7] = EmptyPiece()

board.board[7][0] = KingPiece(7, 0, BLACK)
board.board[7][1] = EmptyPiece()
board.board[7][2] = KingPiece(7, 2, BLACK)
board.board[7][3] = EmptyPiece()
board.board[7][4] = Piece(7, 4, RED)
board.board[7][5] = EmptyPiece()
board.board[7][6] = KingPiece(7, 6, BLACK)
board.board[7][7] = EmptyPiece()

# board.board[0][5] = EmptyPiece()
# board.board[4][2] = Piece(4,2, RED)
# board.board[6][3] = EmptyPiece()
# board.board[6][7] = EmptyPiece()
# board.board[7][4] = EmptyPiece()
# board.board[3][1] = king
# board.board[4][2] = Piece(4,2, RED)
# board.board[6][3] = EmptyPiece()
# board.board[6][7] = EmptyPiece()
# board.board[7][4] = EmptyPiece()


print_board(board)
print("\n")

possible_king_boards = board.get_possible_boards(RED)
for possible_board in possible_king_boards:
    print_board(possible_board)
    print("\n")



