import random
import time
import math
import board
from history_table import HistoryTable
from transposition_cache import TranspositionCache


class Bounds:
    EXACT = 0
    LOWER_BOUND = 1
    UPPER_BOUND = 2


class CacheValue:
    def __init__(self, bound, score, depth):
        self.bound = bound
        self.score = score
        self.depth = depth


class MTDf:
    def __init__(self):
        self.transposition_table = TranspositionCache()
        self.history_table = HistoryTable()

    def iterative_deepening(self, game_board, depth, ai, player):
        firstGuess = 0
        best_board = game_board
        for d in range(depth):
            firstGuess, best_board = self.mtd(game_board, d, firstGuess, ai, player)
            # timeout return/ break
        return firstGuess, best_board

    def mtd(self, game_board, depth, firstGuess, ai, player):
        score = firstGuess
        best_board = game_board
        upperBound = +math.inf
        lowerBound = -math.inf

        while upperBound > lowerBound:
            if score == lowerBound:
                beta = score + 1
            else:
                beta = score

            score, best_board = self.alpha_beta_with_memory(game_board, beta - 1, beta, depth, True, ai, player)
            if score < beta:
                upperBound = score
            else:
                lowerBound = score
        return score, best_board

    def alpha_beta_with_memory(self, game_board, alpha, beta, depth, maximizer, ai, player):
        # print("-------------------------------------------------------")
        cache = self.transposition_table.retrieve(game_board.board)
        # print(self.transposition_table.get_size())
        if cache is not None and cache.depth >= depth:
            if cache.bound == Bounds.EXACT:
                # print("Exact")
                return cache.score, game_board
            elif cache.bound == Bounds.LOWER_BOUND:
                # print("lower bound")
                if cache.score >= beta:
                    return cache.score, game_board
                alpha = max(alpha, cache.score)
            elif cache.bound == Bounds.UPPER_BOUND:
                # print("upper bound")
                if alpha >= cache.score:
                    return cache.score, game_board
                beta = min(beta, cache.score)
            # time.sleep(5)

        if depth == 0:
            return game_board.get_score_for_player(ai), game_board

        if maximizer:
            valid_boards = game_board.get_possible_boards(ai)  # implementation check
            best_score = -999999999
            if len(valid_boards) == 0:
                return best_score, game_board
            best_board = random.choice(valid_boards)
            t_alpha = alpha
            move_ordered_boards = dict()
            for next_board in valid_boards:
                move_ordered_boards[next_board] = self.history_table.retrieve(next_board.board)
            # for next_board in valid_boards:
            for next_board in sorted(move_ordered_boards.items(), key=lambda k_val: k_val[1], reverse=True):
                score = self.alpha_beta_with_memory(next_board[0], t_alpha, beta, depth - 1, False, ai, player)[0]
                if score > best_score:
                    best_score = score
                    best_board = next_board[0]
                t_alpha = max(t_alpha, best_score)
                if best_score >= beta:
                    break
        else:
            valid_boards = game_board.get_possible_boards(player)
            # self.print_board(game_board)
            best_score = +999999999
            if len(valid_boards) == 0:
                return best_score, game_board
            best_board = random.choice(valid_boards)
            t_beta = beta
            move_ordered_boards = dict()
            for next_board in valid_boards:
                move_ordered_boards[next_board] = self.history_table.retrieve(next_board.board)
            # for next_board in valid_boards:
            for next_board in sorted(move_ordered_boards.items(), key=lambda k_val: k_val[1], reverse=True):
                score = self.alpha_beta_with_memory(next_board[0], alpha, t_beta, depth - 1, True, ai, player)[0]
                if score < best_score:
                    best_score = score
                    best_board = next_board[0]
                t_beta = min(t_beta, best_score)
                if alpha >= best_score:
                    break

        if best_score <= alpha:
            self.transposition_table.store(game_board.board, CacheValue(Bounds.UPPER_BOUND, best_score, depth))
        elif best_score >= beta:
            self.transposition_table.store(game_board.board, CacheValue(Bounds.LOWER_BOUND, best_score, depth))
        else:
            self.transposition_table.store(game_board.board, CacheValue(Bounds.EXACT, best_score, depth))
        self.history_table.store(best_board.board, pow(2, depth))
        return best_score, best_board

    #todo remove this
    def print_board(self, board_to_print):
        # print("--------------------------------------------")
        print("      0 1 2 3 4 5 6 7\n")
        row_number = 0
        for row in board_to_print.board:
            row_pieces = []
            for piece in row:
                row_pieces.append(piece.symbol)
            print(str(row_number) + "    |" + "|".join(row_pieces) + "|")
            row_number = row_number + 1
        # print("---------------------------------------------X")