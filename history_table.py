import time

import game_pieces
import random
from empty_piece import EmptyPiece


class HistoryTable:
    def __init__(self):
        self.history_table = dict()

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

    def store(self, board, rating):
        self.history_table[self.get_hash(board)] = self.history_table.get(self.get_hash(board), 0) + rating

    def retrieve(self, board):
        return self.history_table.get(self.get_hash(board), 0)

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
        return len(self.history_table)

    def print_ratings(self):
        print(self.history_table)