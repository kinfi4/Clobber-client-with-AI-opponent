import math

import pygame as pg

import constants as const
from board import Board
from agent import Agent

pg.mixer.pre_init(22100, -16, 2, 64)
pg.init()

s = pg.mixer.Sound('media/sounds/forbidden-sound.wav')
s.set_volume(0.1)


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

        self.agent = Agent()

    def check_mouse_click(self):
        if pg.mouse.get_pressed(3)[0]:
            rel = pg.mouse.get_rel()
            if math.fabs(rel[0]) < 1 and math.fabs(rel[1]) < 1:
                return

            mouse_pos = pg.mouse.get_pos()
            if not self.cell_chosen and self.board.cell_can_be_chosen(mouse_pos, self.current_player_move):
                self.cell_chosen = True
                self.board.toggle_choose_cell(mouse_pos)
            elif self._human_trying_to_move():
                self.board.human_make_move(pg.mouse.get_pos())
                self.board.unchoose_cell()
                self.current_player_move = const.CheckerType.BLACK
                self.cell_chosen = False
                pg.display.update()

                if self.board.game_is_over():
                    self._draw_game_over()
                    input()

                self._computer_make_move()

                if self.board.game_is_over():
                    self._draw_game_over()
                    input()
            elif self.cell_chosen and self.board.mouse_on_chosen_cell(pg.mouse.get_pos()):
                self.cell_chosen = False
                self.board.toggle_choose_cell(pg.mouse.get_pos())
            else:
                self.board.show_that_move_is_impossible(pg.mouse.get_pos())
                s.play(0, 0, fade_ms=5)

    def main_loop(self):
        self.board.draw_the_board()

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

    def _computer_make_move(self):
        # _, new_board = self.agent.simple_minimax(self.board, 3, const.CheckerType.BLACK)
        # _, new_board = self.agent.minimax(self.board, 3, const.CheckerType.BLACK, float('-inf'), float('inf'))

        # _, new_board = self.agent.negamax(self.board, 3, const.CheckerType.BLACK, float('-inf'), float('inf'))
        # _, new_board = self.agent.nega_scout(self.board, 3, const.CheckerType.BLACK, float('-inf'), float('inf'))
        _, new_board = self.agent.plain_negamax(self.board, 3, const.CheckerType.BLACK)

        self.board = new_board
        self.board.draw_the_board()
        self.current_player_move = const.CheckerType.WHITE

    def _human_trying_to_move(self):
        return self.cell_chosen and self.board.human_can_make_move(pg.mouse.get_pos()) \
               and self.current_player_move == const.CheckerType.WHITE


if __name__ == '__main__':
    game = GameController()
    game.main_loop()
