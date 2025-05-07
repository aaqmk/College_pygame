import pygame as pg

pg.init()
SIZE = WIDTH, HEIGHT = 800, 600
screen = pg.display.set_mode(SIZE)

from my_sprite import Kuplich

FPS = 60
BACKGROUND_COLOR = (0, 0, 0)

clock = pg.time.Clock()
running = True

npc = pg.sprite.Group()
for _ in range(10):
    npc.add(Kuplich())

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    screen.fill(BACKGROUND_COLOR)

    npc.draw(screen)
    npc.update()

    pg.display.flip()
    clock.tick(FPS)
pg.quit()
