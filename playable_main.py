import game_pieces
from algorithm import Algorithm
from board import Board, Direction
from empty_piece import EmptyPiece
from king_piece import KingPiece
from piece import Piece
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


def get_direction_from_string(string):
    direction_result = None
    if string == "LEFT":
        direction_result = Direction.LEFT
    elif string == "RIGHT":
        direction_result = Direction.RIGHT
    elif string == "LEFT_BACKWARDS":
        direction_result = Direction.LEFT_BACKWARDS
    elif string == "RIGHT_BACKWARDS":
        direction_result = Direction.RIGHT_BACKWARDS
    return direction_result


def input_piece(game_board, player):
    piece_string = input("Select a piece by providing the row and column value separated by comma: ")
    position_values = piece_string.split(",")
    row = int(position_values[0])
    col = int(position_values[1])
    while not game_board.piece_is_of_player(row, col, player):
        piece_string = input("There is no piece there or it does't belong to you, select another one: ")
        position_values = piece_string.split(",")
        row = int(position_values[0])
        col = int(position_values[1])
    return game_board.get_piece(row, col)


name = input("Enter your name: ")
# name = "guz"

human_player = Player(True, name, game_pieces.RED_PIECE, game_pieces.RED_KING_PIECE)
ai_player = Player(False, "AI", game_pieces.BLACK_PIECE, game_pieces.BLACK_KING_PIECE)
board = Board(human_player, ai_player)
algorithm = Algorithm()


# This is to try things
"""""# board.board[4][3] = Piece(4, 3, ai_player)
board.board[1][2] = EmptyPiece()
board.board[1][0] = EmptyPiece()
board.board[1][4] = EmptyPiece()
board.board[1][6] = EmptyPiece()

# board.board[2][1] = EmptyPiece()
board.board[2][3] = EmptyPiece()
board.board[2][5] = EmptyPiece()
board.board[2][7] = EmptyPiece()

board.board[0][1] = EmptyPiece()
board.board[0][3] = EmptyPiece()
board.board[0][5] = EmptyPiece()
board.board[0][7] = EmptyPiece()

board.board[5][0] = EmptyPiece()
board.board[5][2] = EmptyPiece()
board.board[5][4] = EmptyPiece()
board.board[5][6] = EmptyPiece()

board.board[6][3] = EmptyPiece()
board.board[6][5] = EmptyPiece()
board.board[6][7] = EmptyPiece()

board.board[7][0] = EmptyPiece()
board.board[7][2] = EmptyPiece()
board.board[7][4] = EmptyPiece()
board.board[7][6] = EmptyPiece()

board.board[3][2] = KingPiece(3, 2, human_player)"""

print(name + ", you will be playing as X\n")
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
    # If there is only one move just move it, if not, ask for the direction to move from the possible directions.
    if len(possible_move_directions) == 1:
        direction_string = possible_move_directions[0]
    else:
        direction_string = input("Select one of the following directions " + " ".join(possible_move_directions) + " : ")

    # Move the piece
    moved_piece = board.move_piece_in_direction(selected_piece, get_direction_from_string(direction_string))
    # If more pieces can be eaten, eat if there is only one possibility, ask for the direction if there is more than one
    possible_eat_directions = board.get_possible_eating_moves(moved_piece)
    while len(possible_eat_directions) > 0:
        if len(possible_eat_directions) == 1:
            moved_piece = board.move_piece_in_direction(moved_piece, possible_eat_directions[0])
        else:
            print_board(board)
            print("\n")

            direction_string = input("Select one of the following directions " + " ".join(possible_eat_directions) + " : ")
            moved_piece = board.move_piece_in_direction(moved_piece, get_direction_from_string(direction_string))
        possible_eat_directions = board.get_possible_eating_moves(moved_piece)

    print_board(board)
    print("\n")

    # Check if the human move wasn't the win move
    if board.get_winner() is not None:
        break

    board = algorithm.iterative_deepening(board, 3, ai_player, human_player)[1]

    print("AI Played: \n")
    print_board(board)
    print("\n")

print("The winner is : " + board.get_winner().name + "!!")


















