import time
import game_pieces

from algorithm import Algorithm
from board import Board
from empty_piece import EmptyPiece
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
# board.board[4][1] = Piece(4, 1, top_player)
# board.board[1][0] = EmptyPiece()
# board.board[1][4] = EmptyPiece()


"""for movable_pieces in board.get_movable_pieces(bottom_player):
    possible_boards_for_piece = board.get_possible_boards(movable_pieces)
    for possible_board in possible_boards_for_piece:
        print_board(possible_board)
        print("\n")"""

# possible_boards_for_piece = board.get_possible_boards(board.board[5][0])
# for possible_board in possible_boards_for_piece:
#     print_board(possible_board)
#     print("\n")
#
# print(board.get_score_for_player(top_player))
# print(board.get_score_for_player(bottom_player))
# print(board.get_winner())


board.board[3][2] = Piece(3, 2, RED)
board.board[5][4] = EmptyPiece()

print_board(board)
print("\n")

game = Algorithm()
next_board = game.iterative_deepening(board, 3, BLACK, RED)[1]

print_board(next_board)
print("\n")

next_board.board[3][4] = Piece(3, 4, RED)
next_board.board[5][2] = EmptyPiece()
next_board.board[4][3] = EmptyPiece()

print_board(next_board)
print("\n")

next_board = game.iterative_deepening(next_board, 7, BLACK, RED)[1]

print_board(next_board)
print("\n")

turn = False
times = 1
start = time.time()
while next_board.get_winner() is None:
    if turn:
        next_board = game.iterative_deepening(next_board, 7, BLACK, RED)[1]
    else:
        next_board = game.iterative_deepening(next_board, 7, RED, BLACK)[1]
    times += 1
    # print(next_board.maybe_a_winner())
    print_board(next_board)
    turn = not turn
    # time.sleep(3)
    print("\n")

print("average time: ", (time.time() - start) / times)
