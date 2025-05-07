import pygame as pg

from .utils import load_image


class Kuplich(pg.sprite.Sprite):
    IMG = pg.transform.smoothscale(
        load_image('kuplich.webp'),
        (150, 210))
    IMG_FLIPPED = pg.transform.flip(IMG, True, False)
    MASK = pg.mask.from_surface(IMG)
    MASK_FLIPPED = pg.mask.from_surface(IMG_FLIPPED)
    STEP = 10

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance

    @classmethod
    def get_instance(cls):
        return cls.instance

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = self.IMG
        self.mask = self.MASK
        self.rect = self.IMG.get_rect()
        self._coins = 0
        self._health = 100

    @property
    def coins(self):
        return f'{self._coins} $'

    @property
    def health(self):
        return f'{self._health} ❤'

    def damage(self):
        if self._health:
            self._health -= 1
            if self._health == 0:
                self.kill()

    def collide(self, items_group):
        if self._health <= 0:
            return
        for item in pg.sprite.spritecollide(self, items_group, True, pg.sprite.collide_mask):
            match item.__class__.__name__:
                case 'Coin':
                    self._coins += 1
                case 'Bomb':
                    self._health -= 5
                case 'Heart':
                    self._health += 5
        if self._health <= 0:
            self.kill()

    def update(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key in (pg.K_LEFT, pg.K_a):
                    self.image = self.IMG_FLIPPED
                    self.mask = self.MASK_FLIPPED
                elif event.key in (pg.K_RIGHT, pg.K_d):
                    self.image = self.IMG
                    self.mask = self.MASK

        keyboard = pg.key.get_pressed()
        if (keyboard[pg.K_a] or keyboard[pg.K_LEFT]) and self.rect.left > 0:
            self.rect.move_ip(-self.STEP, 0)
        if (keyboard[pg.K_d] or keyboard[pg.K_RIGHT]) and self.rect.right < 800:
            self.rect.move_ip(self.STEP, 0)
