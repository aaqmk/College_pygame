import pygame
from my_sprite import Platform, Character

pygame.init()
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()
running = True

all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
character = None

while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                platform = Platform(*event.pos)
                all_sprites.add(platform)
                platforms.add(platform)
            elif event.button == 3:
                if character:
                    character.rect.center = event.pos
                    character.velocity = 0
                else:
                    character = Character(*event.pos)
                    all_sprites.add(character)
        if event.type == pygame.KEYDOWN and character:
            if event.key == pygame.K_LEFT:
                character.move_left()
            elif event.key == pygame.K_RIGHT:
                character.move_right()

    if character:
        character.update(platforms, dt)

    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
