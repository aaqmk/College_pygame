import random

import pygame as pg

from utils import load_image


class Kuplich(pg.sprite.Sprite):
    IMG = pg.transform.smoothscale(
        load_image('kuplich.png'),
        (150, 150))

    def __init__(self):
        super().__init__()
        self.image = self.IMG
        self.rect = self.IMG.get_rect()
        self.rect.move_ip(random.randrange(500), random.randrange(500))
        self.rotate = None

    def update(self):
        self.rect.move_ip(random.randint(-1, 1), random.randint(-1, 1))
        if self.rotate is not None:
            self.rotate += 5
            self.image = pg.transform.rotate(self.IMG, self.rotate)
            if self.rotate >= 360:
                self.rotate = None
        elif random.random() < 0.002:
            self.rotate = 0
