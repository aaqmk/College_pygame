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

class Character(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 20, 20, (0, 0, 255))
        self.velocity = 0
        self.on_ground = False

    def update(self, platforms, dt):
        self.velocity += 50 * dt
        self.rect.y += self.velocity * dt
        collisions = pygame.sprite.spritecollide(self, platforms, False)
        if collisions:
            self.rect.y = collisions[0].rect.top - self.rect.height // 2
            self.velocity = 0
            self.on_ground = True
        else:
            self.on_ground = False

    def move_left(self):
        self.rect.x -= 10

    def move_right(self):
        self.rect.x += 10
