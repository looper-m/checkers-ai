import game_pieces
from empty_piece import EmptyPiece
from piece import Piece


# TODO: add kings
# TODO: add eating functionality

class Board:
    def __init__(self, bottom_player, top_player, board=None):
        self.RED = bottom_player
        self.BLACK = top_player
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
                            board_row.append(Piece(row, column, self.BLACK))
                        else:
                            board_row.append(EmptyPiece())
                    else:
                        if column % 2 != 0:
                            board_row.append(EmptyPiece())
                        else:
                            board_row.append(Piece(row, column, self.BLACK))
                elif 2 < row < 5:
                    board_row.append(EmptyPiece())
                else:
                    if row == 5 or row == 7:
                        if column % 2 == 0:
                            board_row.append(Piece(row, column, self.RED))
                        else:
                            board_row.append(EmptyPiece())
                    else:
                        if column % 2 == 0:
                            board_row.append(EmptyPiece())
                        else:
                            board_row.append(Piece(row, column, self.RED))
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
                    if piece.player == self.RED:
                        bottom_player_pieces.append(piece)
                    else:
                        top_player_pieces.append(piece)
        if not top_player_pieces:
            return self.RED
        if not bottom_player_pieces:
            return self.BLACK
        return None

    # new, quitting when KING is found. i know its nonsense but the get_winner above never quits
    def maybe_a_winner(self):
        for row in range(8):
            for column in range(8):
                if self.board[row][column].symbol == game_pieces.BLACK_KING_PIECE:
                    return self.BLACK
                elif self.board[row][column].symbol == game_pieces.RED_KING_PIECE:
                    return self.RED
        return None

    def get_possible_boards(self, player):
        movable_pieces = self.get_movable_pieces(player)
        possible_boards = []
        for movable_piece in movable_pieces:
            possible_boards.extend(self.get_possible_boards_for_piece(movable_piece))
        return possible_boards

    def get_movable_pieces(self, player):
        movable_pieces = []
        for row in self.board:
            for piece in row:
                if not type(piece) == EmptyPiece:
                    if piece.player == player:
                        moved_left = piece.move_left()
                        moved_right = piece.move_right()
                        if self.is_in_movable_position(moved_right, False) or self.is_in_movable_position(moved_left, True):
                            movable_pieces.append(piece)
        return movable_pieces

    def get_possible_boards_for_piece(self, piece):
        list_of_boards = []
        moved_left = piece.move_left()
        if self.is_in_movable_position(moved_left, True):
            list_of_boards.extend(self.move_piece(piece, moved_left, True))
            # list_of_boards = self.move_piece(piece, moved_left, True)
        moved_right = piece.move_right()
        if self.is_in_movable_position(moved_right, False):
            list_of_boards.extend(self.move_piece(piece, moved_right, False))
        return list_of_boards

    def is_in_movable_position(self, piece, to_left):
        return self.is_in_valid_empty_position(piece) or self.is_in_eating_position(piece, to_left)

    def is_in_valid_empty_position(self, piece):
        return not self.is_outside_board(piece) and self.is_in_empty_space(piece)

    def is_outside_board(self, piece):
        return piece.row < 0 or piece.row > 7 or piece.col < 0 or piece.col > 7

    def is_in_empty_space(self, piece):
        piece_in_place = self.board[piece.row][piece.col]
        return type(piece_in_place) == EmptyPiece

    def is_in_eating_position(self, piece, moving_to_left):
        if self.is_outside_board(piece):
            return False

        piece_in_place = self.board[piece.row][piece.col]
        # Piece is in a place where there is other piece from the same team
        if type(piece_in_place) == EmptyPiece or piece_in_place.player == piece.player:
            return False
        else:
            # Piece is in a place where there is other piece from the other team
            # Check if I move again in the same direction there is an empty space
            if moving_to_left:
                moved_to_left = piece.move_left()
                return self.is_in_valid_empty_position(moved_to_left)
            else:
                moved_to_right = piece.move_right()
                return self.is_in_valid_empty_position(moved_to_right)

    def move_piece(self, current_piece, new_piece, to_left):
        possible_boards = []
        new_board_matrix = self.copy_board_matrix(self.board)
        piece_in_place_of_new = new_board_matrix[new_piece.row][new_piece.col]
        # Piece is moving to an empty space
        if type(piece_in_place_of_new) == EmptyPiece:
            new_board_matrix[current_piece.row][current_piece.col] = EmptyPiece()
            new_board_matrix[new_piece.row][new_piece.col] = new_piece
            possible_boards.append(Board(self.RED, self.BLACK, new_board_matrix))
            return possible_boards
            # Piece is eating an opposite piece
        else:
            # Eat pieces recursively and add all the possible results
            self.eat_piece(new_board_matrix, possible_boards, current_piece, new_piece, to_left)
            return possible_boards

    def eat_piece(self, matrix, possible_boards, current_piece, new_piece, to_left):
        # Set an empty space in the place where the piece was
        matrix[current_piece.row][current_piece.col] = EmptyPiece()
        # Set an empty space in the place where the other's team piece was
        matrix[new_piece.row][new_piece.col] = EmptyPiece()

        # If eating towards the left
        if to_left:
            # Move the piece to the left
            moved_to_left = new_piece.move_left()
            # Set the piece in that space. It should be an empty space because this method
            # is called after is_eating_position
            matrix[moved_to_left.row][moved_to_left.col] = moved_to_left
            # Create the new board but not append it to the result because it might be possible to keep eating pieces
            new_board = Board(self.RED, self.BLACK, matrix)
            self.try_to_keep_eating(new_board, matrix, possible_boards, moved_to_left)
        else:
            moved_to_right = new_piece.move_right()
            matrix[moved_to_right.row][moved_to_right.col] = moved_to_right
            new_board = Board(self.RED, self.BLACK, matrix)
            self.try_to_keep_eating(new_board, matrix, possible_boards, moved_to_right)

    # Tries to keep eating pieces recursively until there's no possible piece to e at
    def try_to_keep_eating(self, new_board, matrix, possible_boards, piece):
        possible_eating_left = False
        possible_eating_right = False
        # If the piece is able to eat another piece to the left in the new board, eat it
        if new_board.is_in_eating_position(piece.move_left(), True):
            possible_eating_left = True
            new_board.eat_piece(self.copy_board_matrix(matrix), possible_boards, piece, piece.move_left(), True)
        # If the piece is able to eat another piece to the right in the new board, eat it
        if new_board.is_in_eating_position(piece.move_right(), False):
            possible_eating_right = True
            new_board.eat_piece(self.copy_board_matrix(matrix), possible_boards, piece, piece.move_right(), False)
        # If the piece is not able to eat another piece in any direction, append the resulting board
        if not possible_eating_right and not possible_eating_left:
            possible_boards.append(new_board)

    def copy_board_matrix(self, matrix):
        copied = self.create_empty_board_matrix()
        for row in range(8):
            for column in range(8):
                copied[row][column] = matrix[row][column]
        return copied

    def create_empty_board_matrix(self):
        board = []
        for row in range(8):
            board_row = []
            for column in range(8):
                board_row.append(EmptyPiece())
            board.append(board_row)
        return board
