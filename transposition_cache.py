import game_pieces
import random
from empty_piece import EmptyPiece


class TranspositionCache:
    # transposition_table = dict()
    # RED_PIECE = 0
    # BLACK_PIECE = 1
    # RED_KING_PIECE = 2
    # BLACK_KING_PIECE = 3
    def __init__(self):
        self.transposition_table = dict()

        self.RED_PIECE = 0
        self.BLACK_PIECE = 1
        self.RED_KING_PIECE = 2
        self.BLACK_KING_PIECE = 3

        self.zobrist_matrix = []
        for row in range(64):
            zobrist_row = []
            for column in range(4):
                zobrist_row.append(random.getrandbits(256))
            self.zobrist_matrix.append(zobrist_row)

    def store(self, board, cache_value):
        self.transposition_table[self.get_hash(board)] = cache_value

    def retrieve(self, board):
        self.transposition_table.get(self.get_hash(board))

    # def clear_cache(self):
    #     self.transposition_table = dict()  # skips all zobrist inits

    def get_hash(self, board):
        hash_code = 0
        for row in range(8):
            for column in range(8):
                if type(board[row][column]) == EmptyPiece:
                    continue
                if board[row][column] == game_pieces.RED_PIECE:
                    hash_code ^= self.zobrist_matrix[(row * 8) + column][self.RED_PIECE]
                elif board[row][column] == game_pieces.RED_KING_PIECE:
                    hash_code ^= self.zobrist_matrix[(row * 8) + column][self.RED_KING_PIECE]
                elif board[row][column] == game_pieces.BLACK_PIECE:
                    hash_code ^= self.zobrist_matrix[(row * 8) + column][self.BLACK_PIECE]
                elif board[row][column] == game_pieces.BLACK_KING_PIECE:
                    hash_code ^= self.zobrist_matrix[(row * 8) + column][self.BLACK_KING_PIECE]
        return hash_code
