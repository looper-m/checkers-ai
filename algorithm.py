import board
import math

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
    def __int__(self):
        self.transposition_table = dict()

    def iterative_deepening(self, game_board, depth, ai, player2):
        firstGuess = 0
        for d in range(depth):
            firstGuess = self.mtd(game_board, d, firstGuess, ai, player2)
            # timeout return/ break
        return firstGuess

    def mtd(self, game_board, depth, firstGuess, ai, player2):
        score = firstGuess
        upperBound = +math.inf
        lowerBound = -math.inf

        while upperBound > lowerBound:
            if score == lowerBound:
                beta = score + 1
            else:
                beta = score
            score = self.alpha_beta_with_memory(game_board, beta - 1, beta, depth, True, ai, player2)
            if score < beta:
                upperBound = score
            else:
                lowerBound = score
        return score

    def alpha_beta_with_memory(self, game_board, alpha, beta, depth, maximizer, ai, player2):
        cache = self.transposition_table.get(game_board)

        if game_board is not None and cache.depth >= depth:
            if cache.bound == EXACT:
                return cache.score
            elif cache.bound == LOWER_BOUND:
                alpha = max(alpha, cache.score)
                if alpha >= beta:
                    return cache.score
            elif cache.bound == UPPER_BOUND:
                beta = min(beta, cache.score)
                if alpha >= beta:
                    return cache.score

        if depth == 0:
            return game_board.get_score(ai)

        if maximizer:
            score = -math.inf
            t_alpha = alpha
            valid_boards = game_board.get_possible_boards(ai)  # implementation check
            for next_board in valid_boards:
                score = max(score, self.alpha_beta_with_memory(next_board, t_alpha, beta, depth - 1, False))
                t_alpha = max(t_alpha, score)
                if alpha >= beta:
                    break
        else:
            score = +math.inf
            t_beta = beta
            valid_boards = game_board.get_possible_boards(player2)
            for next_board in valid_boards:
                score = min(score, self.alpha_beta_with_memory(next_board, alpha, t_beta, depth - 1, True))
                t_beta = min(t_beta, score)
                if alpha >= beta:
                    break

        if score <= alpha:
            self.transposition_table[game_board] = CacheValue(UPPER_BOUND, score, depth)
        elif score >= beta:
            self.transposition_table[game_board] = CacheValue(LOWER_BOUND, score, depth)
        else:
            self.transposition_table[game_board] = CacheValue(EXACT, score, depth)
        return score
