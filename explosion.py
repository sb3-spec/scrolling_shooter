import pygame
import os
Sprite = pygame.sprite.Sprite
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = int(SCREEN_WIDTH * .8)
GRAVITY = .75

class Explosion(Sprite):
    """Class for the explosion objects"""
    def __init__(self, x, y, scale) -> None:
        Sprite.__init__(self)
        self.images = []
        self.frame_index = 0

        # loading in images for animation

        num_of_frames = len(os.listdir('./assets/explosion'))

        for i in range(num_of_frames):
            img = pygame.image.load(f'./assets/explosion/{i}.png')
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.images.append(img)

        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0
    
    def update(self):
        EXPLOSION_SPEED = 4
        # update explosion animation
        self.counter += 1

        if self.counter >= EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1
            if self.frame_index > 4:
                self.kill()
                return
            self.image = self.images[self.frame_index]