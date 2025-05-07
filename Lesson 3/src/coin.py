import random

import pygame as pg

from .utils import load_image
from .kuplich import Kuplich


class Item(pg.sprite.Sprite):
    IMG = None
    SPEED = 8
    MASK = None

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = self.IMG
        self.rect = self.IMG.get_rect()
        self.rect.bottom = 0
        self.rect.left = random.randrange(0, 800 - self.rect.width)
        self.mask = self.MASK

    def update(self, events):
        self.rect.y += self.SPEED
        if self.rect.top > 600:
            self.self_kill()

    def self_kill(self):
        self.kill()


class Coin(Item):
    IMG = pg.transform.smoothscale(
        load_image('coin.png'),
        (60, 60))
    MASK = pg.mask.from_surface(IMG)

    def self_kill(self):
        super().kill()
        Kuplich.get_instance().damage()


class Bomb(Item):
    IMG = pg.transform.smoothscale(
        load_image('bomb.webp'),
        (60, 60))
    MASK = pg.mask.from_surface(IMG)


class Heart(Item):
    IMG = pg.transform.smoothscale(
        load_image('heart.png'),
        (60, 40))
    MASK = pg.mask.from_surface(IMG)
