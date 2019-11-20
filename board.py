NO_PIECE = ' '
PLAYER_PIECE = 'x'
AI_PIECE = 'o'
KING_PLAYER_PIECE = 'kx'
KING_AI_PIECE = 'ko'

PLAYER_MAP = {
    NO_PIECE: 'NONE',
    PLAYER_PIECE: 'PLAYER',
    AI_PIECE: 'AI',
}

Players = (PLAYER_PIECE, AI_PIECE)


class Board:
    def __init__(self, board=None):
        if board is None:
            self.board = create_start_board()
        else:
            self.board = board

    def get_possible_boards(self, piece):
        list_of_boards = []
        direction = 1
        if piece == AI_PIECE:
            direction = -1

        for row in range(8):
            for column in range(8):
                if self.board[row][column] == piece:
                    # print(row, column)
                    if is_move_possible(self.board, piece, row + direction, column - 1):
                        list_of_boards.append(move_piece(self.board, piece, row, column, row + direction, column - 1))
                    if is_move_possible(self.board, piece, row + direction, column + 1):
                        list_of_boards.append(move_piece(self.board, piece, row, column, row + direction, column + 1))
        return list_of_boards


def create_start_board():
    board = []
    for row in range(8):
        board_row = []
        for column in range(8):
            if row < 3:
                if row == 0 or row == 2:
                    if column % 2 != 0:
                        board_row.append(PLAYER_PIECE)
                    else:
                        board_row.append(NO_PIECE)
                else:
                    if column % 2 != 0:
                        board_row.append(NO_PIECE)
                    else:
                        board_row.append(PLAYER_PIECE)
            elif 2 < row < 5:
                board_row.append(NO_PIECE)
            else:
                if row == 5 or row == 7:
                    if column % 2 == 0:
                        board_row.append(AI_PIECE)
                    else:
                        board_row.append(NO_PIECE)
                else:
                    if column % 2 == 0:
                        board_row.append(NO_PIECE)
                    else:
                        board_row.append(AI_PIECE)
        board.append(board_row)
    return board


def create_empty_board():
    board = []
    for row in range(8):
        board_row = []
        for column in range(8):
            board_row.append(NO_PIECE)
        board.append(board_row)
    return board


def copy_board(board):
    copied = create_empty_board()
    for row in range(8):
        for column in range(8):
            copied[row][column] = board[row][column]
    return copied


def is_move_possible(board, piece, row, column):
    return 0 <= row <= 7 and 0 <= column <= 7 and board[row][column] != piece


def move_piece(board, piece, fromRow, fromColumn, toRow, toColumn):
    cp_board = copy_board(board)
    cp_board[fromRow][fromColumn] = NO_PIECE
    cp_board[toRow][toColumn] = piece
    return Board(cp_board)
