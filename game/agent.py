from copy import copy

from constants import CheckerType


class Agent:
    def __init__(self, difficulty='low'):
        self.difficulty = difficulty

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
