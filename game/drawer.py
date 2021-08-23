import pygame as pg

import constants as const


class MouseOutOfBoard(Exception):
    pass


class Drawer:
    BOARD_MARGIN_TB = 30
    BOARD_MARGIN_RL = 92

    def __init__(self, screen: pg.Surface):
        self.screen = screen
        self.board_size = None
        self.cell_size = None

    def draw_board(self):
        self._draw_borders()

        screen_size = self.screen.get_size()[0]
        self.board_size = screen_size - 2 * self.BOARD_MARGIN_TB
        self.cell_size = self.board_size / 6

        for i in range(6):  # to draw each row
            for k in range(5):  # to draw each column
                color = const.Color.A_BIT_YELLOW_WHITE if (i + k) % 2 == 0 else const.Color.LIGHTER_BLACK
                self.draw_cell_by_index(color, (k, i))

                checker_type = const.CheckerType.WHITE if (i + k) % 2 == 0 else const.CheckerType.BLACK
                self.draw_checker_by_index((k, i), checker_type)

    def draw_checker_by_index(self, pos, checker_type):
        x, y = self.BOARD_MARGIN_RL + pos[0] * self.cell_size, self.BOARD_MARGIN_TB + pos[1] * self.cell_size
        checker_pos = (x + self.cell_size // 2, y + self.cell_size // 2)

        if checker_type == const.CheckerType.WHITE:
            main_color = const.Color.YELLOW_BLACK
            sub_color = const.Color.LIGHT_BLACK
        elif checker_type == const.CheckerType.BLACK:
            main_color = const.Color.LIGHT_BLACK
            sub_color = const.Color.LIGHTER_BLACK
        else:
            return

        radius = self.cell_size//2 - 12

        pg.draw.circle(self.screen, color=main_color, center=checker_pos, radius=radius)
        pg.draw.circle(self.screen, color=sub_color, center=checker_pos, radius=radius//2, width=6)
        pg.draw.circle(self.screen, color=sub_color, center=checker_pos, radius=radius, width=3)

    def draw_cell_by_index(self, color, position):
        x, y = self.BOARD_MARGIN_RL + position[0] * self.cell_size, self.BOARD_MARGIN_TB + position[1] * self.cell_size
        pg.draw.rect(self.screen, color, (x, y, self.cell_size, self.cell_size))

    def mouse_coordinates_to_cell_index(self, mouse_pos):
        x, y = mouse_pos
        x -= self.BOARD_MARGIN_RL
        y -= self.BOARD_MARGIN_TB

        x_index = int(x // self.cell_size)
        y_index = int(y // self.cell_size)

        if x < 0 or y < 0 or x_index > 4 or y_index > 5:
            raise MouseOutOfBoard()

        return x_index, y_index

    def _draw_borders(self):
        screen_w, screen_h = const.SCREEN_SIZE
        boarder_rect = (self.BOARD_MARGIN_RL - 2,
                        self.BOARD_MARGIN_TB - 2,
                        screen_w - self.BOARD_MARGIN_RL * 2 + 5,
                        screen_h - self.BOARD_MARGIN_TB * 2 + 5)

        pg.draw.rect(self.screen, const.Color.BLACK, boarder_rect, 10)

