import pygame as pg

import constants as const
from board import Board

pg.init()


class GameController:
    def __init__(self):
        self.screen = pg.display.set_mode(const.SCREEN_SIZE)
        self.clock = pg.time.Clock()
        self.board = Board(screen=self.screen)

        self.screen.fill(const.Color.WHITE)

        self.current_player_move = const.CheckerType.WHITE
        self.cell_chosen = False

        pg.display.set_caption('Clobber')
        pg.display.set_icon(pg.image.load('./media/icon.gif'))

    def check_mouse_click(self):
        if pg.mouse.get_pressed(3)[0]:
            mouse_pos = pg.mouse.get_pos()
            if not self.cell_chosen and self.board.cell_can_be_chosen(mouse_pos, self.current_player_move):
                self.cell_chosen = True
                self.board.toggle_choose_cell(mouse_pos)
            elif self.cell_chosen and self.board.can_make_move(pg.mouse.get_pos()):
                self.board.make_move(pg.mouse.get_pos())
                self.board.unchoose_cell()
                self.current_player_move = const.CheckerType.WHITE \
                    if self.current_player_move == const.CheckerType.BLACK else const.CheckerType.BLACK
                self.cell_chosen = False

    def main_loop(self):
        self.board.init_table()

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()

            self.check_mouse_click()

            pg.display.update()
            self.clock.tick(const.FPS)


if __name__ == '__main__':
    game = GameController()
    game.main_loop()
