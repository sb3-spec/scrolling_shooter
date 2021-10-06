import pygame
Sprite = pygame.sprite.Sprite
from explosion import Explosion
grenade_img = pygame.image.load("./assets/Icons/grenade.png")
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = int(SCREEN_WIDTH * .8)
GRAVITY = .75


class Grenade(Sprite):
    """Class for the grenade objects"""
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
        dx = self.speed * self.direction
        dy = self.vel_y

        # check collision with floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.speed = 0
        
        # check wall collision
        if self.rect.right + dx > SCREEN_WIDTH or self.rect.left + dx < 0:
            self.direction *= -1
            dx = self.direction * self.speed

        self.rect.x += dx
        self.rect.y += dy


        

        
        
        
    def handle_explosion(self):
        """handles the fuse timer and explosion"""
        # fuse length
        self.timer -= 1
        if self.timer <= 0:
            # create explosion instance
            explosion = Explosion(self.rect.x, self.rect.y, .5)
            self.kill()
            return explosion
        return False

    





        
    
    