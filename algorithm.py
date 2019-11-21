import commons as cm
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

    def iterative_deepening(self, board, depth):
        firstGuess = 0
        for d in range(depth):
            firstGuess = self.mtd(board, d, firstGuess)
            # timeout return/ break
        return firstGuess

    def mtd(self, board, depth, firstGuess):
        score = firstGuess
        upperBound = +math.inf
        lowerBound = -math.inf

        while upperBound > lowerBound:
            if score == lowerBound:
                beta = score + 1
            else:
                beta = score
            score = self.alpha_beta_with_memory(board, beta - 1, beta, depth, True)
            if score < beta:
                upperBound = score
            else:
                lowerBound = score
        return score

    def alpha_beta_with_memory(self, board, alpha, beta, depth, maximizer):
        cache = self.transposition_table.get(board)

        if board is not None and cache.depth >= depth:
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
            # return get_score(board, player)
            pass

        if maximizer:
            score = -math.inf
            t_alpha = alpha
            valid_boards = cm.get_possible_boards(board, cm.AI_PIECE)  # implementation check
            for next_board in valid_boards:
                score = max(score, self.alpha_beta_with_memory(next_board, t_alpha, beta, depth - 1, False))
                t_alpha = max(t_alpha, score)
                if alpha >= beta:
                    break
        else:
            score = +math.inf
            t_beta = beta
            valid_boards = cm.get_possible_boards(board, cm.PLAYER_PIECE)
            for next_board in valid_boards:
                score = min(score, self.alpha_beta_with_memory(next_board, alpha, t_beta, depth - 1, True))
                t_beta = min(t_beta, score)
                if alpha >= beta:
                    break

        if score <= alpha:
            self.transposition_table[board] = CacheValue(UPPER_BOUND, score, depth)
        elif score >= beta:
            self.transposition_table[board] = CacheValue(LOWER_BOUND, score, depth)
        else:
            self.transposition_table[board] = CacheValue(EXACT, score, depth)
        return score
