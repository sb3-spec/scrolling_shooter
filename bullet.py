import pygame
Sprite = pygame.sprite.Sprite
bullet_img = pygame.image.load("./assets/Icons/bullet.png")
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = int(SCREEN_WIDTH * .8)


class Bullet(Sprite):
    """Class for the bullet objects"""
    def __init__(self, x, y, direction) -> None:
        Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
    
    def update(self):
        # move bullet
        self.rect.x += (self.direction * self.speed)
        # check if bullet is off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()