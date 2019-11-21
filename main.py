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


bottom_player = Player(True, "Player 1", "X")
top_player = Player(False, "Player 2", "O")
board = Board(bottom_player, top_player)

board.board[4][1] = Piece(4, 1, top_player)
board.board[1][0] = EmptyPiece()
board.board[1][4] = EmptyPiece()


print_board(board)
print("\n")

"""for movable_pieces in board.get_movable_pieces(bottom_player):
    possible_boards_for_piece = board.get_possible_boards(movable_pieces)
    for possible_board in possible_boards_for_piece:
        print_board(possible_board)
        print("\n")"""

possible_boards_for_piece = board.get_possible_boards(board.board[5][0])
for possible_board in possible_boards_for_piece:
    print_board(possible_board)
    print("\n")


print(board.get_score_for_player(top_player))
print(board.get_score_for_player(bottom_player))
print(board.get_winner())
