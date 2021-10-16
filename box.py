import pygame
from settings import TILE_SIZE
from explosion import Explosion
Sprite = pygame.sprite.Sprite

class Box(Sprite): 
    """Handles box health and explosions"""
    def __init__(self, x, y, img, scale):
        Sprite.__init__(self)
        self.image = img
        self.health = 60
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
    

    def update(self, screen_scroll):
        """Updates decoration position to account for scroll"""
        if self.health > 0:
            self.rect.x += screen_scroll
        

    def handle_explosion(self, grenade_fx, enemy_group, box_group, player):
        if self.health <= 0:
            grenade_fx.play()
            explosion = Explosion(self.rect.x, self.rect.y, 2)
            # do damage to player
            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and \
                abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
                player.health -= 80

            # do damage to enemies
            for enemy in enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and \
                    abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
                    enemy.health -= 80

            for box in box_group:
                if abs(self.rect.centerx - box.rect.centerx) < TILE_SIZE * 2 and \
                    abs(self.rect.centery - box.rect.centery) < TILE_SIZE * 2:
                    box.health = 0
            self.kill()
            return explosion
        return False


