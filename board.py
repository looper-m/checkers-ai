import game_pieces
from empty_piece import EmptyPiece
from king_piece import KingPiece
from piece import Piece


class MoveKind:
    NORMAL = 0
    EATING = 1
    CROWNED = 2


class Direction:
    RIGHT = "RIGHT"
    LEFT = "LEFT"
    RIGHT_BACKWARDS = "RIGHT_BACKWARDS"
    LEFT_BACKWARDS = "LEFT_BACKWARDS"


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
                        if type(player) == KingPiece:
                            score = score + 2
                        else:
                            score = score + 1
                    else:
                        if type(player) == KingPiece:
                            score = score - 2
                        else:
                            score = score - 1
        return score

    def get_winner(self):
        red_valid_boards = self.get_possible_boards(self.RED)
        if len(red_valid_boards) == 0:
            return self.BLACK
        black_valid_boards = self.get_possible_boards(self.BLACK)
        if len(black_valid_boards) == 0:
            return self.RED

        top_player_pieces = []
        bottom_player_pieces = []
        # TODO: this can be improved: stop if both lists are not empty. dont even use lists maybe.
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

    # TODO: remove this method
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
                        if type(piece) == Piece:
                            if self.is_in_movable_position(moved_left, Direction.LEFT) or self.is_in_movable_position(
                                    moved_right, Direction.RIGHT):
                                movable_pieces.append(piece)
                        else:
                            moved_left_backwards = piece.move_left_backwards()
                            moved_right_backwards = piece.move_right_backwards()
                            if self.is_in_movable_position(moved_left, Direction.LEFT) or \
                                    self.is_in_movable_position(moved_right, Direction.RIGHT) or \
                                    self.is_in_movable_position(moved_left_backwards, Direction.LEFT_BACKWARDS) or \
                                    self.is_in_movable_position(moved_right_backwards, Direction.RIGHT_BACKWARDS):
                                movable_pieces.append(piece)
        return movable_pieces

    def get_possible_boards_for_piece(self, piece):
        list_of_boards = []
        moved_left = piece.move_left()
        if self.is_in_movable_position(moved_left, Direction.LEFT):
            list_of_boards.extend(self.move_piece(piece, moved_left, Direction.LEFT))
        moved_right = piece.move_right()
        if self.is_in_movable_position(moved_right, Direction.RIGHT):
            list_of_boards.extend(self.move_piece(piece, moved_right, Direction.RIGHT))
        if type(piece) == KingPiece:
            moved_left_backwards = piece.move_left_backwards()
            if self.is_in_movable_position(moved_left_backwards, Direction.LEFT_BACKWARDS):
                list_of_boards.extend(self.move_piece(piece, moved_left_backwards, Direction.LEFT_BACKWARDS))
            moved_right_backwards = piece.move_right_backwards()
            if self.is_in_movable_position(moved_right_backwards, Direction.RIGHT_BACKWARDS):
                list_of_boards.extend(self.move_piece(piece, moved_right_backwards, Direction.RIGHT_BACKWARDS))
        return list_of_boards

    def is_in_movable_position(self, piece, direction):
        return self.is_in_valid_empty_position(piece) or self.is_in_eating_position(piece, direction)

    def is_in_valid_empty_position(self, piece):
        return not self.is_outside_board(piece) and self.is_in_empty_space(piece)

    def is_outside_board(self, piece):
        return piece.row < 0 or piece.row > 7 or piece.col < 0 or piece.col > 7

    def is_in_empty_space(self, piece):
        piece_in_place = self.board[piece.row][piece.col]
        return type(piece_in_place) == EmptyPiece

    def is_in_eating_position(self, piece, direction):
        if self.is_outside_board(piece):
            return False

        piece_in_place = self.board[piece.row][piece.col]
        # Piece is in a place where there is other piece from the same team
        if type(piece_in_place) == EmptyPiece or piece_in_place.player == piece.player:
            return False
        else:
            # Piece is in a place where there is other piece from the other team
            # Check if I move again in the same direction there is an empty space
            if direction == Direction.LEFT:
                moved_to_left = piece.move_left()
                return self.is_in_valid_empty_position(moved_to_left)
            if direction == Direction.RIGHT:
                moved_to_right = piece.move_right()
                return self.is_in_valid_empty_position(moved_to_right)
            if direction == Direction.LEFT_BACKWARDS:
                moved_to_left_backwards = piece.move_left_backwards()
                return self.is_in_valid_empty_position(moved_to_left_backwards)
            if direction == Direction.RIGHT_BACKWARDS:
                moved_to_right_backwards = piece.move_right_backwards()
                return self.is_in_valid_empty_position(moved_to_right_backwards)

    def move_piece(self, current_piece, new_piece, direction):
        possible_boards = []
        new_board_matrix = self.copy_board_matrix(self.board)
        piece_in_place_of_new = new_board_matrix[new_piece.row][new_piece.col]
        # Piece is moving to an empty space
        if type(piece_in_place_of_new) == EmptyPiece:
            new_board_matrix[current_piece.row][current_piece.col] = EmptyPiece()
            new_board_matrix[new_piece.row][new_piece.col] = new_piece
            possible_boards.append(Board(self.RED, self.BLACK, new_board_matrix))
            # if type(new_piece) == KingPiece and type(current_piece) == Piece:
            #     possible_boards.append([Board(self.RED, self.BLACK, new_board_matrix), MoveKind.CROWNED])
            # else:
            #     possible_boards.append([Board(self.RED, self.BLACK, new_board_matrix), MoveKind.NORMAL])
            return possible_boards
            # Piece is eating an opposite piece
        else:
            # Eat pieces recursively and add all the possible results
            self.eat_piece(new_board_matrix, possible_boards, current_piece, new_piece, direction)
            return possible_boards

    def eat_piece(self, matrix, possible_boards, current_piece, new_piece, direction):
        # Set an empty space in the place where the piece was
        matrix[current_piece.row][current_piece.col] = EmptyPiece()
        # Set an empty space in the place where the other's team piece was
        matrix[new_piece.row][new_piece.col] = EmptyPiece()

        # If eating towards the left
        if direction == Direction.LEFT:
            # Move the piece to the left
            moved_to_left = new_piece.move_left()
            # Set the piece in that space. It should be an empty space because this method
            # is called after is_eating_position
            matrix[moved_to_left.row][moved_to_left.col] = moved_to_left
            # Create the new board but not append it to the result because it might be possible to keep eating pieces
            new_board = Board(self.RED, self.BLACK, matrix)
            self.try_to_keep_eating(new_board, matrix, possible_boards, moved_to_left)
        elif direction == Direction.RIGHT:
            moved_to_right = new_piece.move_right()
            matrix[moved_to_right.row][moved_to_right.col] = moved_to_right
            new_board = Board(self.RED, self.BLACK, matrix)
            self.try_to_keep_eating(new_board, matrix, possible_boards, moved_to_right)
        elif direction == Direction.LEFT_BACKWARDS:
            moved_to_left_backwards = new_piece.move_left_backwards()
            matrix[moved_to_left_backwards.row][moved_to_left_backwards.col] = moved_to_left_backwards
            new_board = Board(self.RED, self.BLACK, matrix)
            self.try_to_keep_eating(new_board, matrix, possible_boards, moved_to_left_backwards)
        elif direction == Direction.RIGHT_BACKWARDS:
            moved_to_right_backwards = new_piece.move_right_backwards()
            matrix[moved_to_right_backwards.row][moved_to_right_backwards.col] = moved_to_right_backwards
            new_board = Board(self.RED, self.BLACK, matrix)
            self.try_to_keep_eating(new_board, matrix, possible_boards, moved_to_right_backwards)

    # Tries to keep eating pieces recursively until there's no possible piece to e at
    def try_to_keep_eating(self, new_board, matrix, possible_boards, piece):
        possible_eating_left = False
        possible_eating_right = False
        # If the piece is able to eat another piece to the left in the new board, eat it
        if new_board.is_in_eating_position(piece.move_left(), Direction.LEFT):
            possible_eating_left = True
            new_board.eat_piece(self.copy_board_matrix(matrix), possible_boards, piece, piece.move_left(),
                                Direction.LEFT)
        # If the piece is able to eat another piece to the right in the new board, eat it
        if new_board.is_in_eating_position(piece.move_right(), Direction.RIGHT):
            possible_eating_right = True
            new_board.eat_piece(self.copy_board_matrix(matrix), possible_boards, piece, piece.move_right(),
                                Direction.RIGHT)

        if type(piece) == Piece:
            # If the piece is not able to eat another piece in any direction, append the resulting board
            if not possible_eating_right and not possible_eating_left:
                possible_boards.append(new_board)
                # possible_boards.append([new_board, MoveKind.EATING])
        # For the king we also need to try keep eating backwards
        else:
            possible_eating_left_backwards = False
            possible_eating_right_backwards = False
            if new_board.is_in_eating_position(piece.move_left_backwards(), Direction.LEFT_BACKWARDS):
                possible_eating_left_backwards = True
                new_board.eat_piece(self.copy_board_matrix(matrix), possible_boards, piece, piece.move_left_backwards(),
                                    Direction.LEFT_BACKWARDS)
            if new_board.is_in_eating_position(piece.move_right_backwards(), Direction.RIGHT_BACKWARDS):
                possible_eating_right = True
                new_board.eat_piece(self.copy_board_matrix(matrix), possible_boards, piece,
                                    piece.move_right_backwards(),
                                    Direction.RIGHT_BACKWARDS)
            if not possible_eating_right and not possible_eating_left and not possible_eating_left_backwards and not possible_eating_right_backwards:
                possible_boards.append(new_board)
                # possible_boards.append([new_board, MoveKind.EATING])

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

    # -------- Helper methods for user input ------------ #

    def piece_is_of_player(self, row, col, player):
        piece = self.board[row][col]
        return type(piece) is not EmptyPiece and piece.player == player

    def get_piece(self, row, col):
        return self.board[row][col]

    def get_piece_pos(self,piece):
        return (piece.row,piece.col)

    def get_piece_symbol(self,row,col):
        piece = self.board[row][col]
        return piece.symbol

    def possible_move_directions(self, piece):
        directions = []
        moved_left = piece.move_left()
        moved_right = piece.move_right()
        if self.is_in_movable_position(moved_left, Direction.LEFT):
            directions.append(Direction.LEFT)
        if self.is_in_movable_position(moved_right, Direction.RIGHT):
            directions.append(Direction.RIGHT)
        if type(piece) == KingPiece:
            moved_left_backwards = piece.move_left_backwards()
            moved_right_backwards = piece.move_right_backwards()
            if self.is_in_movable_position(moved_left_backwards, Direction.LEFT_BACKWARDS):
                directions.append(Direction.LEFT_BACKWARDS)
            if self.is_in_movable_position(moved_right_backwards, Direction.RIGHT_BACKWARDS):
                directions.append(Direction.RIGHT_BACKWARDS)
        return directions

    def move_piece_in_direction(self, piece, direction):
        moved_piece = None
        if direction == Direction.LEFT:
            moved_piece = piece.move_left()
        elif direction == Direction.RIGHT:
            moved_piece = piece.move_right()
        elif direction == Direction.LEFT_BACKWARDS:
            moved_piece = piece.move_left_backwards()
        elif direction == Direction.RIGHT_BACKWARDS:
            moved_piece = piece.move_right_backwards()
        return self.move_piece_in_board(piece, moved_piece, direction)

    def move_piece_in_board(self, current_piece, new_piece, direction):
        piece_in_place = self.board[new_piece.row][new_piece.col]
        # Piece is moving to an empty space
        if type(piece_in_place) == EmptyPiece:
            self.board[current_piece.row][current_piece.col] = EmptyPiece()
            self.board[new_piece.row][new_piece.col] = new_piece
            # First argument is if a piece was eaten
            return False, new_piece
        # Piece is eating an opposite piece
        else:
            # Eat pieces recursively and add all the possible results
            return True, self.eat_piece_in_board(current_piece, new_piece, direction)

    def eat_piece_in_board(self, current_piece, new_piece, direction):
        # Set an empty space in the place where the piece was
        self.board[current_piece.row][current_piece.col] = EmptyPiece()
        # Set an empty space in the place where the other's team piece was
        self.board[new_piece.row][new_piece.col] = EmptyPiece()

        # If eating towards the left
        if direction == Direction.LEFT:
            # Move the piece to the left
            moved_to_left = new_piece.move_left()
            # Set the piece in that space. It should be an empty space because this method
            # is called after is_eating_position
            self.board[moved_to_left.row][moved_to_left.col] = moved_to_left
            return moved_to_left
        elif direction == Direction.RIGHT:
            moved_to_right = new_piece.move_right()
            self.board[moved_to_right.row][moved_to_right.col] = moved_to_right
            return moved_to_right
        elif direction == Direction.LEFT_BACKWARDS:
            moved_to_left_backwards = new_piece.move_left_backwards()
            self.board[moved_to_left_backwards.row][moved_to_left_backwards.col] = moved_to_left_backwards
            return moved_to_left_backwards
        elif direction == Direction.RIGHT_BACKWARDS:
            moved_to_right_backwards = new_piece.move_right_backwards()
            self.board[moved_to_right_backwards.row][moved_to_right_backwards.col] = moved_to_right_backwards
            return moved_to_right_backwards

    def get_possible_eating_moves(self, piece):
        directions = []
        if self.is_in_eating_position(piece.move_left(), Direction.LEFT):
            directions.append(Direction.LEFT)
        if self.is_in_eating_position(piece.move_right(), Direction.RIGHT):
            directions.append(Direction.RIGHT)
        if type(piece) == KingPiece:
            if self.is_in_eating_position(piece.move_left_backwards(), Direction.LEFT_BACKWARDS):
                directions.append(Direction.LEFT_BACKWARDS)
            if self.is_in_eating_position(piece.move_right_backwards(), Direction.RIGHT_BACKWARDS):
                directions.append(Direction.RIGHT_BACKWARDS)
        return directions