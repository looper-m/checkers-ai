from empty_piece import EmptyPiece
from piece import Piece


# TODO: add kings
# TODO: add eating functionality

class Board:
    def __init__(self, bottom_player, top_player, board=None):
        self.bottom_player = bottom_player
        self.top_player = top_player
        if board is None:
            self.board = self.create_start_board()
        else:
            self.board = board

    def create_start_board(self):
        board = []
        for row in range(8):
            board_row = []
            for column in range(8):
                if row < 3:
                    if row == 0 or row == 2:
                        if column % 2 != 0:
                            board_row.append(Piece(row, column, self.top_player))
                        else:
                            board_row.append(EmptyPiece())
                    else:
                        if column % 2 != 0:
                            board_row.append(EmptyPiece())
                        else:
                            board_row.append(Piece(row, column, self.top_player))
                elif 2 < row < 5:
                    board_row.append(EmptyPiece())
                else:
                    if row == 5 or row == 7:
                        if column % 2 == 0:
                            board_row.append(Piece(row, column, self.bottom_player))
                        else:
                            board_row.append(EmptyPiece())
                    else:
                        if column % 2 == 0:
                            board_row.append(EmptyPiece())
                        else:
                            board_row.append(Piece(row, column, self.bottom_player))
            board.append(board_row)
        return board

    def get_score_for_player(self, player):
        score = 0
        for row in self.board:
            for piece in row:
                if not type(piece) == EmptyPiece:
                    if piece.player == player:
                        score = score + 1
                    else:
                        score = score - 1
        return score

    def get_winner(self):
        top_player_pieces = []
        bottom_player_pieces = []
        #TODO: this can be improved: stop if both lists are not empty. dont even use lists maybe.
        for row in self.board:
            for piece in row:
                if not type(piece) == EmptyPiece:
                    if piece.player == self.bottom_player:
                        bottom_player_pieces.append(piece)
                    else:
                        top_player_pieces.append(piece)
        if not top_player_pieces:
            return self.bottom_player
        if not bottom_player_pieces:
            return self.top_player
        return None

    def get_movable_pieces(self, player):
        movable_pieces = []
        for row in self.board:
            for piece in row:
                if not type(piece) == EmptyPiece:
                    if piece.player == player:
                        moved_left = piece.move_left()
                        moved_right = piece.move_right()
                        if self.is_in_valid_position(moved_right) or self.is_in_valid_position(moved_left):
                            movable_pieces.append(piece)
        return movable_pieces

    def get_possible_boards(self, piece):
        list_of_boards = []
        moved_left = piece.move_left()
        if self.is_in_valid_position(moved_left):
            list_of_boards.append(self.move_piece(piece, moved_left))
        moved_right = piece.move_right()
        if self.is_in_valid_position(moved_right):
            list_of_boards.append(self.move_piece(piece, moved_right))
        return list_of_boards

    def is_in_valid_position(self, piece):
        if piece.row < 0 or piece.row > 7 or piece.col < 0 or piece.col > 7:
            return False
        else:
            return type(self.board[piece.row][piece.col]) == EmptyPiece

    def move_piece(self, old_piece, new_piece):
        new_board = self.copy_board()
        new_board[old_piece.row][old_piece.col] = EmptyPiece()
        new_board[new_piece.row][new_piece.col] = new_piece
        return Board(self.bottom_player, self.top_player, new_board)

    def copy_board(self):
        copied = self.create_empty_board()
        for row in range(8):
            for column in range(8):
                copied[row][column] = self.board[row][column]
        return copied

    def create_empty_board(self):
        board = []
        for row in range(8):
            board_row = []
            for column in range(8):
                board_row.append(EmptyPiece())
            board.append(board_row)
        return board
