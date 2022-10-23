from copy import copy

from constants import CheckerType


class Agent:
    def __init__(self, difficulty='low'):
        self.difficulty = difficulty

    def plain_negamax(self, board, depth: int, color_making_move):
        if depth == 0 or board.game_is_over():
            return -board.evaluate_board(), board

        max_eval = float('-inf')
        best_board = None
        previous_color = CheckerType.BLACK if color_making_move == CheckerType.WHITE else CheckerType.WHITE
        for new_board in self.get_all_moves(board, color_making_move):
            new_evaluation = self.plain_negamax(new_board, depth - 1, previous_color)[0]

            if new_evaluation > max_eval:
                max_eval = new_evaluation
                best_board = new_board

        return -max_eval, best_board

    def negamax(self, board, depth: int, color_making_move, i_alpha, i_beta):
        if depth == 0 or board.game_is_over():
            return -board.evaluate_board(), board

        max_eval = float('-inf')
        best_board = None
        previous_color = CheckerType.BLACK if color_making_move == CheckerType.WHITE else CheckerType.WHITE
        for new_board in self.get_all_moves(board, color_making_move):
            new_evaluation = self.negamax(new_board, depth - 1, previous_color, -i_beta, -i_alpha)[0]

            if new_evaluation > max_eval:
                max_eval = new_evaluation
                best_board = new_board

            i_alpha = max(new_evaluation, i_alpha)
            if i_beta <= i_alpha:
                break

        return -max_eval, best_board

    def nega_scout(self, board, depth: int, color_making_move, i_alpha, i_beta):
        if depth == 0 or board.game_is_over():
            return -board.evaluate_board(), board

        max_eval = float('-inf')
        best_board = None
        b = i_beta
        previous_color = CheckerType.BLACK if color_making_move == CheckerType.WHITE else CheckerType.WHITE

        for board_idx, new_board in enumerate(self.get_all_moves(board, color_making_move)):
            new_evaluation = self.nega_scout(new_board, depth - 1, previous_color, -b, -i_alpha)[0]

            if i_alpha < new_evaluation < i_beta and board_idx > 0:
                new_evaluation = self.nega_scout(new_board, depth - 1, previous_color, -i_beta, -i_alpha)[0]

            if new_evaluation > max_eval:
                max_eval = new_evaluation
                best_board = new_board

            i_alpha = max(new_evaluation, i_alpha)
            if i_beta <= i_alpha:
                break

            b = i_alpha + 1

        return -max_eval, best_board

    def simple_minimax(self, board, depth, color_making_move):
        if depth == 0 or board.game_is_over():
            return board.evaluate_board(), board

        best_board = None

        if color_making_move == CheckerType.WHITE:
            max_eval = float('-inf')
            for new_board in self.get_all_moves(board, color_making_move):
                evaluation, _ = self.simple_minimax(new_board, depth - 1, CheckerType.BLACK)

                if evaluation > max_eval:
                    max_eval = evaluation
                    best_board = new_board

            return max_eval, best_board

        else:
            min_eval = float('inf')
            for new_board in self.get_all_moves(board, color_making_move):
                evaluation, _ = self.simple_minimax(new_board, depth - 1, CheckerType.WHITE)

                if evaluation < min_eval:
                    min_eval = evaluation
                    best_board = new_board

            return min_eval, best_board

    def minimax(self, board, depth, color_making_move, i_alpha, i_beta):
        if depth == 0 or board.game_is_over():
            return board.evaluate_board(), board

        best_board = None

        if color_making_move == CheckerType.BLACK:  # we have to maximize the evaluation
            for new_board in self.get_all_moves(board, color_making_move):
                evaluation, _ = self.minimax(new_board, depth - 1, CheckerType.WHITE, i_alpha, i_beta)

                if evaluation > i_alpha:
                    i_alpha = evaluation
                    best_board = new_board

                if i_alpha > i_beta:
                    break

            return i_alpha, best_board
        else:  # we have to minimize the evaluation
            for new_board in self.get_all_moves(board, color_making_move):
                evaluation, _ = self.minimax(new_board, depth - 1, CheckerType.BLACK, i_alpha, i_beta)

                if evaluation < i_beta:
                    i_beta = evaluation
                    best_board = new_board

                if i_alpha > i_beta:
                    break

            return i_beta, best_board

    def get_all_moves(self, board, color):
        moves = []

        for cell in board.get_all_cells(color):
            valid_moves = board.get_valid_moves(*cell)

            for move in valid_moves:
                temp_board = copy(board)
                temp_board.make_move(cell, move, False)
                moves.append(temp_board)

        return moves
