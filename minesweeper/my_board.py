import enum
import random

import pygame as pg

from board import Board
from utils import load_image

CLOSED = -1
MINE = 10
FLAG = 110
QUESTION = 220


class Status(enum.Enum):
    NOT_INITIALIZED = 0
    PLAYING = 1
    WINNING = 2
    LOSING = 3


class Minesweeper(Board):
    """
    0       - 0 мин вокруг (открытая клетка)
    1..8    - 1-8 мин вокруг (открытая клетка)
    -1      - закрытая клетка (не мина)
    10      - мина
    +100    - флажок
    +200    - вопрос
    """

    CELL_COLOR = pg.Color('#818181')
    DOUBLE_CLICK_DELAY = 500  # мс

    def __init__(self, width: int, height: int, count_mines: int):
        super().__init__(width, height, initial_value=CLOSED)
        self._count_mines = count_mines
        self._status = Status.NOT_INITIALIZED
        self._show_mines = False
        self._no_mines = self._width * self._height - count_mines
        font = pg.font.Font(None, round(self._cell_size * 1.2))
        self._DIGITS = [
            font.render(str(i), True, color)
            for i, color in enumerate([
                'black', 'blue', 'green', 'orange', 'black', 'darkviolet', 'saddlebrown', 'maroon', 'red'
            ])
        ]
        self._IMAGE_QUESTION = font.render('?', True, 'black')
        self._IMAGE_BOMB = pg.transform.smoothscale(
            load_image('bomb.png'),
            (self._cell_size, self._cell_size)
        )
        self._IMAGE_FLAG = pg.transform.smoothscale(
            load_image('flag.png'),
            (self._cell_size, self._cell_size)
        )
        self._double_click_clock = pg.time.Clock()
        self._last_coord = None

    def draw_cell(self, screen: pg.Surface, row: int, col: int, rect: pg.Rect) -> None:
        cell = self._board[row][col]
        if cell == MINE and self._show_mines:
            screen.blit(self._IMAGE_BOMB, rect.topleft)
        elif cell == CLOSED or cell == MINE and not self._show_mines or cell >= 100:
            pg.draw.rect(screen, '#505050', rect)
            if cell // 100 == 1:
                screen.blit(self._IMAGE_FLAG, rect.topleft)
            elif cell // 100 == 2:
                screen.blit(self._IMAGE_QUESTION, (
                    rect.centerx - self._IMAGE_QUESTION.get_width() // 2,
                    rect.centery - self._IMAGE_QUESTION.get_height() // 2
                ))
        elif 0 < cell <= 8:
            digit = self._DIGITS[cell]
            screen.blit(digit, (
                rect.centerx - digit.get_width() // 2,
                rect.centery - digit.get_height() // 2
            ))

    def on_click(self, row: int, col: int) -> None:
        if row < 0 or col < 0 or row >= self._height or col >= self._width:
            return
        if self._status == Status.WINNING or self._status == Status.LOSING:
            return
        if self._status == Status.NOT_INITIALIZED:
            self._initial(row, col)
        cell = self._board[row][col]
        if 0 <= cell <= 8:
            return
        elif cell == MINE:
            self._lose()
        elif cell == CLOSED:
            self._no_mines -= 1
            self._board[row][col] = self._get_neighbours(row, col)
            if self._board[row][col] == 0:
                self._open_neighbours(row, col)
            if self._no_mines == 0:
                self._win()

    def _open_neighbours(self, row: int, col: int) -> None:
        for x in range(col - 1, col + 2):
            for y in range(row - 1, row + 2):
                if x != col or y != row:
                    self.on_click(y, x)

    def _get_neighbours(self, row: int, col: int) -> int:
        result = 0
        for x in range(col - 1, col + 2):
            for y in range(row - 1, row + 2):
                if self.get_cell(y, x) in (MINE, MINE + QUESTION, MINE + FLAG):
                    result += 1
        return result

    def _win(self) -> None:
        self._status = Status.WINNING
        print('win')

    def _lose(self) -> None:
        self._status = Status.LOSING
        self._show_mines = True
        print('lose')

    def _initial(self, row: int, col: int) -> None:
        self._status = Status.PLAYING
        n = 0
        assert self._count_mines < self._width * self._height
        while n < self._count_mines:
            x = random.randrange(self._width)
            y = random.randrange(self._height)
            if (y, x) != (row, col) and self._board[y][x] == CLOSED:
                self._board[y][x] = MINE
                n += 1

    def handle_event(self, event: pg.event.Event) -> None:
        if event.type == pg.MOUSEBUTTONDOWN:
            coord = self.get_at(*event.pos)
            if coord:
                if event.button == 1:
                    if self._double_click_clock.tick() < self.DOUBLE_CLICK_DELAY and coord == self._last_coord :
                        self.on_double_click(*coord)
                    else:
                        self.on_click(*coord)
                    self._last_coord = coord
                elif event.button == 3:
                    self.on_right_click(*coord)

    def on_double_click(self, row: int, col: int) -> None:
        if self._status == Status.WINNING or self._status == Status.LOSING:
            return
        if 1 <= self._board[row][col] <= 8:
            count_flags = 0
            for x in range(col - 1, col + 2):
                for y in range(row - 1, row + 2):
                    if self.get_cell(y, x) in (FLAG, FLAG + MINE):
                        count_flags += 1
            if count_flags == self._board[row][col]:
                for x in range(col - 1, col + 2):
                    for y in range(row - 1, row + 2):
                        self.on_click(y, x)

    def on_right_click(self, row: int, col: int) -> None:
        if self._status == Status.WINNING or self._status == Status.LOSING:
            return
        if self._status == Status.NOT_INITIALIZED:
            return
        if self._board[row][col] in (CLOSED, MINE):
            self._board[row][col] += 110  # ставим флаг
        elif self._board[row][col] // 100 == 1:
            self._board[row][col] += 110  # ставим вопрос
        elif self._board[row][col] // 100 == 2:
            self._board[row][col] -= 220  # снимаем вопрос
