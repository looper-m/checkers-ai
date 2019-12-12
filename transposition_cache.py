import time

import game_pieces
import random
from empty_piece import EmptyPiece


class TranspositionCache:
    def __init__(self):
        self.transposition_table = dict()

        self.RED_PIECE = 0
        self.BLACK_PIECE = 1
        self.RED_KING_PIECE = 2
        self.BLACK_KING_PIECE = 3

        self.zobrist_matrix = []
        for row in range(8):
            zobrist_row = []
            for column in range(8):
                zobrist_column = []
                for piece in range(4):
                    zobrist_column.append(random.getrandbits(128))
                zobrist_row.append(zobrist_column)
            self.zobrist_matrix.append(zobrist_row)

    def store(self, board, cache_value):
        # print(self.get_hash(board))
        # time.sleep(5)
        # print()
        self.transposition_table[self.get_hash(board)] = cache_value

    def retrieve(self, board):
        # print("the hash im trying to retrieve", self.get_hash(board))
        # print("the contents of hash table ",self.transposition_table)
        # time.sleep(2)
        # print()
        return self.transposition_table.get(self.get_hash(board))

    # def clear_cache(self):
    #     self.transposition_table = dict()  # skips all zobrist inits

    def get_hash(self, board):
        hash_code = 0
        for row in range(8):
            for column in range(8):
                if type(board[row][column]) == EmptyPiece:
                    continue
                # print(board[row][column].symbol)
                if board[row][column].symbol == game_pieces.RED_PIECE:
                    hash_code ^= self.zobrist_matrix[row][column][self.RED_PIECE]
                elif board[row][column].symbol == game_pieces.RED_KING_PIECE:
                    hash_code ^= self.zobrist_matrix[row][column][self.RED_KING_PIECE]
                elif board[row][column].symbol == game_pieces.BLACK_PIECE:
                    hash_code ^= self.zobrist_matrix[row][column][self.BLACK_PIECE]
                elif board[row][column].symbol == game_pieces.BLACK_KING_PIECE:
                    hash_code ^= self.zobrist_matrix[row][column][self.BLACK_KING_PIECE]
        return hash_code

    def get_size(self):
        return len(self.transposition_table)

    def printcache(self):
        print(self.transposition_table)