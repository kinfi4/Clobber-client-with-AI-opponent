import math

import pygame as pg

import constants as const
from drawer import Drawer, MouseOutOfBoard


class Board:
    def __init__(self, screen: pg.Surface):
        self.screen = screen
        self.drawer = Drawer(screen=screen)

        self.board_matrix = [
            [const.CheckerType.WHITE if (i + k) % 2 == 0 else const.CheckerType.BLACK for k in range(5)]
            for i in range(6)
        ]

        self.chosen_cell = None

    def init_table(self):
        self.drawer.draw_board()

    def can_make_move(self, final_position):
        if not self.chosen_cell:
            return False

        try:
            x_final, y_final = self.drawer.mouse_coordinates_to_cell_index(final_position)
        except MouseOutOfBoard:
            return False

        x_chosen, y_chosen = self.chosen_cell

        if math.fabs(x_final - x_chosen) > 1 or math.fabs(y_final - y_chosen) > 1:
            return False
        if math.fabs(x_final - x_chosen) == 1 and math.fabs(y_final - y_chosen) == 1:
            return False
        if self.board_matrix[y_chosen][x_chosen] == self.board_matrix[y_final][x_final]:  # cant eat checker with the same color
            return False
        if self.board_matrix[y_final][x_final] == const.CheckerType.EMPTY:  # cant set checker to the empty cell
            return False

        return True

    def make_move(self, final_position):
        x_final, y_final = self.drawer.mouse_coordinates_to_cell_index(final_position)
        x_chosen, y_chosen = self.chosen_cell

        checker_type = self.board_matrix[y_chosen][x_chosen]

        self.board_matrix[y_chosen][x_chosen] = const.CheckerType.EMPTY
        self.board_matrix[y_final][x_final] = checker_type

        self.drawer.draw_checker_by_index((x_final, y_final), checker_type)

    def toggle_choose_cell(self, mouse_position):
        x_final, y_final = self.drawer.mouse_coordinates_to_cell_index(mouse_position)

        if (x_final, y_final) == self.chosen_cell:  # we have to unchoose the cell
            cell_color = const.Color.A_BIT_YELLOW_WHITE if (y_final + x_final) % 2 == 0 else const.Color.LIGHTER_BLACK
            self.chosen_cell = None
        else:
            cell_color = const.Color.CHOSEN_WHITE
            self.chosen_cell = (x_final, y_final)

        self.drawer.draw_cell_by_index(cell_color, (x_final, y_final))

        checker_type = self.board_matrix[y_final][x_final]
        self.drawer.draw_checker_by_index((x_final, y_final), checker_type)

    def mouse_on_chosen_cell(self, mouse_position) -> bool:
        try:
            x_final, y_final = self.drawer.mouse_coordinates_to_cell_index(mouse_position)
        except MouseOutOfBoard:
            return False

        print(self.chosen_cell, x_final, y_final)
        return (x_final, y_final) == self.chosen_cell

    def unchoose_cell(self):
        x_final, y_final = self.chosen_cell
        color = const.Color.A_BIT_YELLOW_WHITE if (y_final + x_final) % 2 == 0 else const.Color.LIGHTER_BLACK
        self.drawer.draw_cell_by_index(color, (x_final, y_final))
        self.chosen_cell = None

    def cell_can_be_chosen(self, mouse_position, color_making_move):
        try:
            x_final, y_final = self.drawer.mouse_coordinates_to_cell_index(mouse_position)
        except MouseOutOfBoard:
            return False

        return self.board_matrix[y_final][x_final] == color_making_move

    def game_is_over(self, current_turn):
        for y in range(len(self.board_matrix)):
            for x in range(len(self.board_matrix[0])):
                if self.board_matrix[y][x] == current_turn:
                    if self._cell_can_make_move(x, y):
                        return False

        return True

    def _cell_can_make_move(self, x, y):
        checker_type = self.board_matrix[y][x]
        target_type = const.CheckerType.BLACK if checker_type == const.CheckerType.WHITE else const.CheckerType.WHITE

        results = []
        if y > 0:
            results.append(self.board_matrix[y - 1][x])
        if x > 0:
            results.append(self.board_matrix[y][x - 1])
        if x < len(self.board_matrix[0]) - 1:
            results.append(self.board_matrix[y][x + 1])
        if y < len(self.board_matrix) - 1:
            results.append(self.board_matrix[y + 1][x])

        return target_type in results
