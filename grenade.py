import pygame

from character import GRAVITY
Sprite = pygame.sprite.Sprite
grenade_img = pygame.image.load("./assets/Icons/grenade.png")
SCREEN_WIDTH = 1000
GRAVITY = .75
SCREEN_HEIGHT = int(SCREEN_WIDTH * .8)


class Grenade(Sprite):
    """Class for the bullet objects"""
    def __init__(self, x, y, direction) -> None:
        Sprite.__init__(self)
        self.speed = 10
        self.timer = 100
        self.vel_y = -10
        self.image = grenade_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
    
    def update(self):
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        self.rect.x += self.speed * self.direction
        self.rect.y += self.vel_y

        if self.rect.bottom > 300:
            self.kill()



