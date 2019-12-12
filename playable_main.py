import game_pieces
from algorithm import Algorithm
from MTDf import MTDf
from board import Board, Direction
from empty_piece import EmptyPiece
from king_piece import KingPiece
from piece import Piece
from player import Player
import view

def movement(old_row,old_col):
    new_pos = view.get_pos()
    new_row = new_pos[0]
    new_col = new_pos[1]
    print(new_row, new_col)
    direction_string = None
    if old_row - 1 == new_row and old_col - 1 == new_col:
        direction_string = "left"
    elif old_row - 1 == new_row and old_col + 1 == new_col:
        direction_string = "right"
    elif old_row + 1 == new_row and old_col - 1 == new_col and (board.get_piece_symbol(old_row, old_col) == "X̂"):
        direction_string = "left backwards"
    elif old_row + 1 == new_row and old_col + 1 == new_col and (board.get_piece_symbol(old_row, old_col) == "X̂"):
        direction_string = "right backwards"
    elif old_row - 2 == new_row and old_col - 2 == new_col and (
            board.get_piece_symbol(old_row - 1, old_col - 1) == "O" or board.get_piece_symbol(old_row - 1,
                                                                                              old_col - 1) == "Ô̂"):
        direction_string = "left"
    elif old_row - 2 == new_row and old_col + 2 == new_col and (
            board.get_piece_symbol(old_row - 1, old_col + 1) == "O" or board.get_piece_symbol(old_row - 1,
                                                                                              old_col + 1) == "Ô"):
        direction_string = "right"
    elif old_row + 2 == new_row and old_col - 2 == new_col and (
            board.get_piece_symbol(old_row + 1, old_col - 1) == "O" or board.get_piece_symbol(old_row + 1,
                                                                                              old_col - 1) == "Ô" and (
                    board.get_piece_symbol(old_row, old_col) == "X̂")):
        direction_string = "left backwards"
    elif old_row + 2 == new_row and old_col + 2 == new_col and (
            board.get_piece_symbol(old_row + 1, old_col + 1) == "O" or board.get_piece_symbol(old_row + 1,
                                                                                              old_col + 1) == "Ô" and (
                    board.get_piece_symbol(old_row, old_col) == "X̂")):
        direction_string = "right backwards"
    return direction_string


def print_board(board_to_print):
    print("      0 1 2 3 4 5 6 7\n")
    row_number = 0
    for row in board_to_print.board:
        row_pieces = []
        for piece in row:
            row_pieces.append(piece.symbol)
        print(str(row_number) + "    |" + "|".join(row_pieces) + "|")
        row_number = row_number + 1


def get_direction_from_string(string):
    l_string = string.lower()
    direction_result = None
    if l_string in ("l", "left"):
        direction_result = Direction.LEFT
    elif l_string in ("r", "right"):
        direction_result = Direction.RIGHT
    elif l_string in ("left_backwards", "left backwards", "left back", "lb", "l b"):
        direction_result = Direction.LEFT_BACKWARDS
    elif l_string in ("right_backwards", "right backwards", "right back", "rb", "r b"):
        direction_result = Direction.RIGHT_BACKWARDS
    return direction_result


def input_piece(game_board, player):
    # piece_string = input("Select a piece by providing the row and column value separated by comma: ")
    # position_values = piece_string.split(",")
    # row = int(position_values[0])
    # col = int(position_values[1])
    # print(row,col)
    pos = view.get_pos()
    row = pos[0]
    col = pos[1]
    print(row,col)
    while not game_board.piece_is_of_player(row, col, player):
        # piece_string = input("There is no piece there or it does't belong to you, select another one: ")
        # position_values = piece_string.split(",")
        # row = int(position_values[0])
        # col = int(position_values[1])
        print("There is no piece there or it does't belong to you, select another one: ")
        pos = view.get_pos()
        row = pos[0]
        col = pos[1]
    return game_board.get_piece(row, col)





# TODO: remove this, is to try things
"""board.board[3][4] = Piece(3, 4, ai_player)
board.board[5][2] = Piece(5, 2, ai_player)
board.board[3][2] = Piece(3, 2, ai_player)
board.board[1][2] = EmptyPiece()
board.board[1][0] = EmptyPiece()
board.board[1][4] = EmptyPiece()
board.board[1][6] = EmptyPiece()
board.board[2][1] = EmptyPiece()
board.board[2][3] = EmptyPiece()
board.board[2][5] = EmptyPiece()
board.board[2][7] = EmptyPiece()
board.board[0][1] = EmptyPiece()
board.board[0][3] = EmptyPiece()
board.board[0][5] = EmptyPiece()
board.board[0][7] = EmptyPiece()
board.board[5][0] = EmptyPiece()
# board.board[5][2] = EmptyPiece()
board.board[5][4] = EmptyPiece()
board.board[5][6] = EmptyPiece()
board.board[6][3] = EmptyPiece()
board.board[6][5] = EmptyPiece()
board.board[6][7] = EmptyPiece()
board.board[7][0] = EmptyPiece()
board.board[7][2] = EmptyPiece()
board.board[7][4] = EmptyPiece()
board.board[7][6] = EmptyPiece()
# board.board[3][2] = KingPiece(3, 2, human_player)"""


# name = input("Enter your name: ")
# name = "guz"

name = view.choosename()
human_player = Player(True, name, game_pieces.RED_PIECE, game_pieces.RED_KING_PIECE)
ai_player = Player(False, "AI", game_pieces.BLACK_PIECE, game_pieces.BLACK_KING_PIECE)
board = Board(human_player, ai_player)
# algorithm = Algorithm()
algorithm = MTDf()
print(name + ", you will be playing as X\n")
view.draw(board)
print_board(board)
print("\n")

while board.get_winner() is None:

    selected_piece = input_piece(board, human_player)
    possible_move_directions = board.possible_move_directions(selected_piece)
    while not possible_move_directions:
        print("The selected piece is not able to move anywhere.")
        selected_piece = input_piece(board, human_player)
        possible_move_directions = board.possible_move_directions(selected_piece)

    direction_string = None
    direction = None
    old_row = None
    old_col = None
    # If there is only one move just move it, if not, ask for the direction to move from the possible directions.
    if len(possible_move_directions) == 1:
        direction_string = possible_move_directions[0]
    else:
        selected_piece_pos = board.get_piece_pos(selected_piece)
        old_row = selected_piece_pos[0]
        old_col = selected_piece_pos[1]
        # direction_string = input("Select one of the following directions " + " ".join(possible_move_directions) + " : ")
        while direction_string is None:
             direction_string = movement(old_row,old_col)

    # Move the piece
    eaten, moved_piece = board.move_piece_in_direction(selected_piece, get_direction_from_string(direction_string))
    # If a piece was eaten and more pieces can be eaten, eat if there is only one possibility,
    # ask for the direction if there is more than one
    if eaten:
        possible_eat_directions = board.get_possible_eating_moves(moved_piece)
        while len(possible_eat_directions) > 0:
            if len(possible_eat_directions) == 1:
                moved_piece = board.move_piece_in_direction(moved_piece, possible_eat_directions[0])[1]
            else:
                print_board(board)
                view.redraw(board)
                print("\n")

                selected_piece_pos = board.get_piece_pos(selected_piece)
                old_row = selected_piece_pos[0]
                old_col = selected_piece_pos[1]
                # direction_string = input("Select one of the following directions " + " ".join(possible_eat_directions) + " : ")
                direction_string = None
                while direction_string is None:
                    direction_string = movement(old_row, old_col)
                    
                moved_piece = board.move_piece_in_direction(moved_piece, get_direction_from_string(direction_string))[1]
            possible_eat_directions = board.get_possible_eating_moves(moved_piece)

    print_board(board)
    view.redraw(board)
    print("\n")

    # Check if the human move wasn't the win move
    if board.get_winner() is not None:
        break

    board = algorithm.iterative_deepening(board, 3, ai_player, human_player)[1]

    print("AI Played: \n")
    print_board(board)
    view.redraw(board)
    print("\n")

print("The winner is : " + board.get_winner().name + "!!")
view.winner(board.get_winner().name)