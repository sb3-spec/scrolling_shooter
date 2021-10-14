import pygame
Sprite = pygame.sprite.Sprite
from explosion import Explosion
from settings import SCREEN_HEIGHT, SCREEN_WIDTH, GRAVITY, TILE_SIZE
grenade_img = pygame.image.load("./assets/Icons/grenade.png")

class Grenade(Sprite):
    """Class for the grenade objects"""
    def __init__(self, x, y, direction) -> None:
        Sprite.__init__(self)
        self.speed = 8
        self.timer = 100
        self.vel_y = -10
        self.image = grenade_img
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
    
    def update(self, world, screen_scroll):
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dx = self.speed * self.direction
        dy = self.vel_y

        # check collision with obstacles
        for tile in world.obstacle_list:
            # check in x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                self.direction *= -1
                dx = self.speed * self.direction
            # check in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # check if grenade has upward momentum
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                elif self.vel_y >= 0: # check if grenade if falling
                    self.vel_y = 0
                    dy = tile[1].top - self.rect.bottom
                    self.speed = 0
        
        # check wall collision
        if self.rect.right + dx > SCREEN_WIDTH or self.rect.left + dx < 0:
            self.direction *= -1
            dx = self.direction * self.speed

        self.rect.x += dx
        self.rect.y += dy

        #scroll
        self.rect.x += screen_scroll
        
        
    def handle_explosion(self, player, enemy_group):
        """handles the fuse timer and explosion"""
        # fuse length
        self.timer -= 1
        if self.timer <= 0:
            # create explosion instance
            explosion = Explosion(self.rect.x, self.rect.y, 2)
            self.kill()
            # do damage to player
            print(player.health)
            if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and \
                abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
                player.health -= 50

            # do damage to enemies
            for enemy in enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and \
                    abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
                    enemy.health -= 50

            return explosion
        return False


# from main import player



        
    
    