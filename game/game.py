import math
from time import sleep

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
            rel = pg.mouse.get_rel()
            if math.fabs(rel[0]) < 1 and math.fabs(rel[1]) < 1:
                return

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

                if self.board.game_is_over(self.current_player_move):
                    self._draw_game_over()
                    input()

            elif self.cell_chosen and self.board.mouse_on_chosen_cell(pg.mouse.get_pos()):
                self.cell_chosen = False
                self.board.toggle_choose_cell(pg.mouse.get_pos())

    def main_loop(self):
        self.board.init_table()

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()

            self.check_mouse_click()

            pg.display.update()
            self.clock.tick(const.FPS)

    def _draw_game_over(self):
        font = pg.font.SysFont('liberationmono', 60)
        game_over_text = font.render('GAME OVER', True, const.Color.LIGHT_RED, const.Color.WHITE)

        s_w, s_h = const.SCREEN_SIZE
        pos_game_over = game_over_text.get_rect(center=(s_w//2, s_h//2))

        winner = const.CheckerType.WHITE if self.current_player_move == const.CheckerType.BLACK else const.CheckerType.BLACK
        winning_string = 'White is a winner' if winner == const.CheckerType.WHITE else 'Black is a winner'
        winning_text = font.render(winning_string, True, const.Color.LIGHT_RED, const.Color.WHITE)
        pos_winner_text = winning_text.get_rect(center=(s_w//2, s_h//2 + 100))

        self.screen.blit(game_over_text, pos_game_over)
        self.screen.blit(winning_text, pos_winner_text)
        pg.display.update()


if __name__ == '__main__':
    game = GameController()
    game.main_loop()
