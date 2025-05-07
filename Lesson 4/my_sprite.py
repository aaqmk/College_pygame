import pygame


class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))


class Platform(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 10, (128, 128, 128))


class Ladder(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 10, 50, (255, 0, 0))


class Character(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 20, 20, (0, 0, 255))
        self.velocity = 0
        self.on_ladder = False

    def update(self, platforms, ladders, dt):
        ladder_collisions = pygame.sprite.spritecollide(self, ladders, False)

        if ladder_collisions:
            self.on_ladder = True
            self.velocity = 0
        else:
            self.on_ladder = False
            self.velocity += 50 * dt
            self.rect.y += self.velocity * dt

            platform_collisions = pygame.sprite.spritecollide(self, platforms, False)
            if platform_collisions:
                self.rect.y = platform_collisions[0].rect.top - self.rect.height // 2
                self.velocity = 0

    def move_left(self):
        self.rect.x -= 10

    def move_right(self):
        self.rect.x += 10

    def move_up(self):
        if self.on_ladder:
            self.rect.y -= 10

    def move_down(self):
        if self.on_ladder:
            self.rect.y += 10
