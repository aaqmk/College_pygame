import pygame as pg

from board import Board


class Game(Board):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # TODO

    def draw_cell(self, screen: pg.Surface, row: int, col: int, rect: pg.Rect) -> None:
        if self._board[row][col] == 0:
            color = pg.Color('white')
        else:
            color = pg.Color('black')
        pg.draw.circle(screen, color, rect.center, rect.w * 0.4)

    def on_click(self, row: int, col: int) -> None:
        # TODO: Проверить, что мы можем сходить в эту клетку
        # Это лишь пример. Код должен быть другой
        self._board[row][col] = 1 - self._board[row][col]
