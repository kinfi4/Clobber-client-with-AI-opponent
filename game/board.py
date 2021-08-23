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

        x_index, y_index = self.chosen_cell

        if self.board_matrix[y_index][x_index] == self.board_matrix[y_final][x_final]:  # cant eat checker with the same color
            return False
        if self.board_matrix[y_final][x_final] == const.CheckerType.EMPTY:  # cant set checker to the empty cell
            return False

        return True

    def make_move(self, final_position):
        x_final, y_final = self.drawer.mouse_coordinates_to_cell_index(final_position)
        x_chosen, y_chosen = self.chosen_cell

        checker_type = self.board_matrix[y_chosen][x_chosen]

        self.board_matrix[y_chosen][x_chosen] = const.CheckerType.EMPTY
        self.board_matrix[y_final][x_chosen] = checker_type

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
