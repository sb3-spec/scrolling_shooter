import pygame

from settings import TILE_SIZE
Sprite = pygame.sprite.Sprite

class Decoration(Sprite):
    """Decorations object class"""
    def __init__(self, img, x, y):
        Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
    
    def update(self, scren_scroll):
        """Updates decoration position to account for scroll"""
        self.rect.x += scren_scroll

class Water(Sprite):
    """Water objects"""
    def __init__(self, img, x, y, scale):
        Sprite.__init__(self)
        self.image = img
        img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
    
    def update(self, scren_scroll):
        """Updates water position to account for scroll"""
        self.rect.x += scren_scroll

class Exit(Sprite):
    """Exit objects"""
    def __init__(self, img, x, y):
        Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
    
    def update(self, scren_scroll):
        """Updates water position to account for scroll"""
        self.rect.x += scren_scroll

    