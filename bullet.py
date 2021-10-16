import pygame
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
Sprite = pygame.sprite.Sprite
bullet_img = pygame.image.load("./assets/Icons/bullet.png")



class Bullet(Sprite):
    """Class for the bullet objects"""
    def __init__(self, x, y, direction, bullet_group) -> None:
        Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        self.bullet_group = bullet_group
    
    def update(self, player, enemy_group, world, screen_scroll, box_group):
        # move bullet
        self.rect.x += (self.direction * self.speed + screen_scroll)
        # check if bullet is off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        
        # check collision with characters
        if pygame.sprite.spritecollide(player, self.bullet_group, False):
            if player.alive:
                player.health -= 34
                self.kill()
        
        # check collision with obstacles
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()

        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, self.bullet_group, False):
                if enemy.alive:
                    enemy.health -= 34
                    self.kill()

        for box in box_group:
            if pygame.sprite.spritecollide(box, self.bullet_group, False):
                if box.alive:
                    box.health -= 34
                    self.kill()