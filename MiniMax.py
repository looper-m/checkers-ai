import random


class MiniMax():
    def minimax_alphabeta(self, game_board, depth, alpha, beta, maximizer, ai, player):
        if depth == 0:
            return game_board.get_score_for_player(ai), game_board

        if maximizer:
            valid_boards = game_board.get_possible_boards(ai)
            # print(depth)
            best_score = -999999999
            if len(valid_boards) == 0:
                return best_score, game_board
            best_board = random.choice(valid_boards)
            for next_board in valid_boards:
                score = self.minimax_alphabeta(next_board, depth - 1, alpha, beta, False, ai, player)[0]
                if score > best_score:
                    best_score = score
                    best_board = next_board
                alpha = max(alpha, best_score)
                if alpha >= beta:
                    return best_score, best_board
            return best_score, best_board

        else:
            valid_boards = game_board.get_possible_boards(player)
            best_score = +999999999
            if len(valid_boards) == 0:
                return best_score, game_board
            best_board = random.choice(valid_boards)
            for next_board in valid_boards:
                score = self.minimax_alphabeta(next_board, depth - 1, alpha, beta, True, ai, player)[0]
                if score < best_score:
                    best_score = score
                    best_board = next_board
                beta = min(beta, best_score)
                if alpha >= beta:
                    return best_score, best_board
            return best_score, best_board