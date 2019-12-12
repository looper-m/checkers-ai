import time
import math
from transposition_cache import TranspositionCache

# try for enum
EXACT = 0
LOWER_BOUND = 1
UPPER_BOUND = 2


class CacheValue:
    def __init__(self, bound, score, depth):
        self.bound = bound
        self.score = score
        self.depth = depth


class Algorithm:
    loop = 0

    def __init__(self):
        self.transposition_table = TranspositionCache()

    def iterative_deepening(self, game_board, depth, ai, player2):
        firstGuess = 0
        best_board = game_board
        for d in range(depth):
            firstGuess, best_board = self.mtd(game_board, d, firstGuess, ai, player2)
            # timeout return/ break
        return firstGuess, best_board

    def mtd(self, game_board, depth, firstGuess, ai, player2):
        score = firstGuess
        best_board = game_board
        upperBound = +math.inf
        lowerBound = -math.inf

        while upperBound > lowerBound:
            if score == lowerBound:
                beta = score + 1
            else:
                beta = score
            score, best_board = self.alpha_beta_with_memory(game_board, beta - 1, beta, depth, True, ai, player2)
            if score < beta:
                upperBound = score
            else:
                lowerBound = score
        return score, best_board

    def alpha_beta_with_memory(self, game_board, alpha, beta, depth, maximizer, ai, player2):
        # print("-------------------------------------------------------")
        cache = self.transposition_table.retrieve(game_board.board)
        # print(self.transposition_table.get_size())
        if cache is not None and cache.depth >= depth:
            if cache.bound == EXACT:
                print("Exact")
                return cache.score, game_board
            elif cache.bound == LOWER_BOUND:
                # print("lower bound")
                alpha = max(alpha, cache.score)
                if alpha >= beta:
                    return cache.score, game_board
            elif cache.bound == UPPER_BOUND:
                # print("upper bound")
                beta = min(beta, cache.score)
                if alpha >= beta:
                    return cache.score, game_board
            # time.sleep(5)

        if depth == 0:
            return game_board.get_score_for_player(ai), game_board

        if maximizer:
            valid_boards = game_board.get_possible_boards(ai)  # implementation check
            best_score = -math.inf
            best_board = game_board
            t_alpha = alpha
            for next_board in valid_boards:
                score = self.alpha_beta_with_memory(next_board, t_alpha, beta, depth - 1, False, ai, player2)[0]
                if score > best_score:
                    best_score = score
                    best_board = next_board
                t_alpha = max(t_alpha, best_score)
                if best_score >= beta:
                    break
        else:
            valid_boards = game_board.get_possible_boards(player2)
            best_score = +math.inf
            best_board = game_board
            t_beta = beta
            for next_board in valid_boards:
                score = self.alpha_beta_with_memory(next_board, alpha, t_beta, depth - 1, True, ai, player2)[0]
                if score < best_score:
                    best_score = score
                    best_board = next_board
                t_beta = min(t_beta, best_score)
                if alpha >= best_score:
                    break
        # Algorithm.loop +=1
        # print("looping ", Algorithm.loop)
        if best_score <= alpha:
            self.transposition_table.store(game_board.board, CacheValue(UPPER_BOUND, best_score, depth))
        elif best_score >= beta:
            self.transposition_table.store(game_board.board, CacheValue(LOWER_BOUND, best_score, depth))
        else:
            self.transposition_table.store(game_board.board, CacheValue(EXACT, best_score, depth))
        return best_score, best_board