import math
from time import sleep
from copy import deepcopy

import pygame as pg

from constants import CheckerType, Color
from drawer import Drawer, MouseOutOfBoard


class Board:
    def __init__(self, screen: pg.Surface, init_board_matrix=None):
        self.screen = screen
        self.drawer = Drawer(screen=screen)

        if init_board_matrix is None:
            self.board_matrix = [
                [CheckerType.WHITE if (y + x) % 2 == 0 else CheckerType.BLACK for x in range(5)]
                for y in range(6)]
        else:
            self.board_matrix = init_board_matrix

        self.chosen_cell = None

    def draw_the_board(self):
        self.drawer.draw_board(self.board_matrix)

    def human_can_make_move(self, final_position):
        try:
            x_final, y_final = self.drawer.mouse_coordinates_to_cell_index(final_position)
        except MouseOutOfBoard:
            return False

        x_chosen, y_chosen = self.chosen_cell

        return self.move_is_possible((x_chosen, y_chosen), (x_final, y_final))

    def move_is_possible(self, pos1, pos2):
        x_chosen, y_chosen = pos1
        x_final, y_final = pos2

        if math.fabs(x_final - x_chosen) > 1 or math.fabs(y_final - y_chosen) > 1:
            return False
        if math.fabs(x_final - x_chosen) == 1 and math.fabs(y_final - y_chosen) == 1:
            return False
        if self.board_matrix[y_chosen][x_chosen] == self.board_matrix[y_final][x_final]:  # cant eat checker with the same color
            return False
        if self.board_matrix[y_final][x_final] == CheckerType.EMPTY:  # cant set checker to the empty cell
            return False

        return True

    def human_make_move(self, final_position):
        x_final, y_final = self.drawer.mouse_coordinates_to_cell_index(final_position)
        x_chosen, y_chosen = self.chosen_cell

        self.make_move((x_chosen, y_chosen), (x_final, y_final))

    def make_move(self, pos1, pos2, drawing=True):
        x_chosen, y_chosen = pos1
        x_final, y_final = pos2

        checker_type = self.board_matrix[y_chosen][x_chosen]

        self.board_matrix[y_chosen][x_chosen] = CheckerType.EMPTY
        self.board_matrix[y_final][x_final] = checker_type

        if drawing:
            self.drawer.draw_checker_by_index((x_final, y_final), checker_type)

    def toggle_choose_cell(self, mouse_position):
        x_final, y_final = self.drawer.mouse_coordinates_to_cell_index(mouse_position)

        if (x_final, y_final) == self.chosen_cell:  # we have to unchoose the cell
            cell_color = Color.A_BIT_YELLOW_WHITE if (y_final + x_final) % 2 == 0 else Color.LIGHTER_BLACK
            self.chosen_cell = None
        else:
            cell_color = Color.CHOSEN_WHITE
            self.chosen_cell = (x_final, y_final)

        self.drawer.draw_cell_by_index(cell_color, (x_final, y_final))

        checker_type = self.board_matrix[y_final][x_final]
        self.drawer.draw_checker_by_index((x_final, y_final), checker_type)

    def mouse_on_chosen_cell(self, mouse_position) -> bool:
        try:
            x_final, y_final = self.drawer.mouse_coordinates_to_cell_index(mouse_position)
        except MouseOutOfBoard:
            return False

        return (x_final, y_final) == self.chosen_cell

    def unchoose_cell(self):
        x_final, y_final = self.chosen_cell
        color = Color.A_BIT_YELLOW_WHITE if (y_final + x_final) % 2 == 0 else Color.LIGHTER_BLACK
        self.drawer.draw_cell_by_index(color, (x_final, y_final))
        self.chosen_cell = None

    def cell_can_be_chosen(self, mouse_position, color_making_move):
        try:
            x_final, y_final = self.drawer.mouse_coordinates_to_cell_index(mouse_position)
        except MouseOutOfBoard:
            return False

        return self.board_matrix[y_final][x_final] == color_making_move

    def game_is_over(self):
        for x, y in self.get_all_cells(CheckerType.WHITE):  # it doesnt matter what color to use,
            if not self.cell_is_dead(x, y):        # if there is a move for white there will for black as well
                return False

        return True

    def show_that_move_is_impossible(self, mouse_position):
        try:
            x_final, y_final = self.drawer.mouse_coordinates_to_cell_index(mouse_position)
        except MouseOutOfBoard:
            return

        initial_color = Color.A_BIT_YELLOW_WHITE if (y_final + x_final) % 2 == 0 else Color.LIGHTER_BLACK
        self.drawer.draw_cell_by_index(Color.LIGHT_RED, (x_final, y_final))
        self.drawer.draw_checker_by_index((x_final, y_final), self.board_matrix[y_final][x_final])
        pg.display.update()

        sleep(0.2)

        self.drawer.draw_cell_by_index(initial_color, (x_final, y_final))
        self.drawer.draw_checker_by_index((x_final, y_final), self.board_matrix[y_final][x_final])
        pg.display.update()

    def get_valid_moves(self, x, y) -> list:
        checker_type = self.board_matrix[y][x]
        target_type = CheckerType.BLACK if checker_type == CheckerType.WHITE else CheckerType.WHITE

        moves = []

        if x > 0 and self.board_matrix[y][x - 1] == target_type:
            moves.append((x - 1, y))
        if y > 0 and self.board_matrix[y - 1][x] == target_type:
            moves.append((x, y - 1))
        if y < len(self.board_matrix) - 1 and self.board_matrix[y + 1][x] == target_type:
            moves.append((x, y + 1))
        if x < len(self.board_matrix[0]) - 1 and self.board_matrix[y][x + 1] == target_type:
            moves.append((x + 1, y))

        return moves

    def get_all_cells(self, color):
        for y in range(6):
            for x in range(5):
                if self.board_matrix[y][x] == color:
                    yield x, y

    def cell_is_dead(self, x, y):
        return len(self.get_valid_moves(x, y)) == 0

    def evaluate_board(self):
        n_of_white, n_of_black = 0, 0

        for y in range(len(self.board_matrix)):
            for x in range(len(self.board_matrix[0])):
                if self.board_matrix[y][x] == CheckerType.WHITE and self.cell_is_dead(x, y):
                    n_of_white += 1
                if self.board_matrix[y][x] == CheckerType.BLACK and self.cell_is_dead(x, y):
                    n_of_black += 1

        return n_of_black - n_of_white

    def __copy__(self):
        return Board(self.screen, init_board_matrix=deepcopy(self.board_matrix))
