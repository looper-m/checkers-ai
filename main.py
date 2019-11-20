from board import create_start_board, get_possible_boards, PLAYER_PIECE


def print_board(board):
    for row in board:
        print('|' + '|'.join(row) + '|')


Board = create_start_board()
print_board(Board)
lis = get_possible_boards(Board, PLAYER_PIECE)
for x in lis:
    print_board(x)
    print("\n")
