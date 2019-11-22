from board import Board
from player import Player


def print_board(board_to_print):
    print("      0 1 2 3 4 5 6 7\n")
    row_number = 0
    for row in board_to_print.board:
        row_pieces = []
        for piece in row:
            row_pieces.append(piece.symbol)
        print(str(row_number) + "    |" + "|".join(row_pieces) + "|")
        row_number = row_number + 1


def input_piece(game_board, human_player):
    piece_string = input("Select a piece by providing the row and column value separated by comma: ")
    position_values = piece_string.split(",")
    row = int(position_values[0])
    col = int(position_values[1])
    while not game_board.piece_is_of_player(row, col, human_player):
        piece_string = input("There is no piece there or it does't belong to you, select another one: ")
        position_values = piece_string.split(",")
        row = int(position_values[0])
        col = int(position_values[1])
    return game_board.get_piece(row, col)


# name = input("Enter your name: ")
name = "guz"

bottom_player = Player(True, name, "X")
top_player = Player(False, "AI", "O")
board = Board(bottom_player, top_player)

print(name + ", you will be playing as X\n")
print_board(board)
print("\n")

selected_piece = input_piece(board, bottom_player)








