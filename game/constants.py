from enum import Enum


SCREEN_SIZE = (800, 800)
FPS = 30


class Color:
    BLACK = (4, 4, 4)
    YELLOW_BLACK = (250, 240, 190)

    LIGHT_BLACK = (70, 70, 70)
    LIGHTER_BLACK = (30, 30, 30)
    WHITE = (245, 245, 245)
    A_BIT_YELLOW_WHITE = (233, 233, 233)
    CHOSEN_WHITE = (245, 180, 180)


class CheckerType(Enum):
    BLACK = 1
    WHITE = 0
    EMPTY = -1
