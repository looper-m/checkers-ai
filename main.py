from board import PLAYER_PIECE, Board


def print_board(board_to_print):
    for row in board_to_print.board:
        print('|' + '|'.join(row) + '|')


board = Board()
print_board(board)
lis = board.get_possible_boards(PLAYER_PIECE)
for x in lis:
    print_board(x)
    print("\n")
