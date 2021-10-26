import pygame
import os
from settings import SCROLL_THRESH, TILE_SIZE, screen, SCREEN_HEIGHT
from character import Character
from healthbar import HealthBar
from itembox import ItemBox
from decorations import Water, Decoration, Exit

from box import Box


pine1_img = pygame.image.load('./assets/background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('./assets/background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('./assets/background/mountain.png').convert_alpha()
sky_img = pygame.image.load('./assets/background/sky_cloud.png').convert_alpha()

class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data, enemy_group, item_box_group, water_group, decoration_group, exit_group, box_group):
        """Turns world_data into a level"""
        tile_list = self.load_images()

        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                self.level_length = len(row)
                if tile >= 0:
                    img = tile_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if (tile >= 0 and tile <= 8):
                        self.obstacle_list.append(tile_data)
                    elif tile == 12:
                        box = Box(img_rect.x, img_rect.y, img, 1)
                        box_group.add(box)
                    elif tile == 9 or tile == 10:
                        water = Water(img, img_rect.x, img_rect.y, .02)
                        water_group.add(water)
                    elif tile >= 11 and tile <= 14:
                        decoration = Decoration(img, img_rect.x, img_rect.y)
                        decoration_group.add(decoration)
                    elif tile == 15:
                        # create player
                        player = Character(screen, "player", img_rect.x, img_rect.y, 1.65, 20, 10, 2)
                        player_health_bar = HealthBar(10, 10, player.health, player.health)
                    elif tile == 16:
                        # create enemies
                        enemy = Character(screen, "enemy", img_rect.x, img_rect.y, 1.65, 20, 10, 1)
                        enemy_group.add(enemy)
                    elif tile == 17:
                        # create ammo box
                        ammo_box = ItemBox("Ammo", img_rect.x, img_rect.y)
                        item_box_group.add(ammo_box)
                    elif tile == 18:
                        # create grenade box
                        ammo_box = ItemBox("Grenade", img_rect.x, img_rect.y)
                        item_box_group.add(ammo_box)
                    elif tile == 19:
                        # create health box 
                        ammo_box = ItemBox("Health", img_rect.x, img_rect.y)
                        item_box_group.add(ammo_box)
                    elif tile == 20:
                        exit = Exit(img, img_rect.x, img_rect.y)
                        exit_group.add(exit)
        return player, player_health_bar

    
    def load_images(self):
        tile_list = []
        num_of_imgs = len(os.listdir("./assets/tiles"))

        i = 0
        for i in range(num_of_imgs):
            img = pygame.image.load(f"./assets/tiles/{i}.png").convert_alpha()
            img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            tile_list.append(img)
        return tile_list
    
    def draw_bg(self, bg_scroll):
        """Draws background images"""
        width = sky_img.get_width()
        
        for i in range(10):
            offset = width * i
            screen.blit(sky_img, (0 - bg_scroll * .5 + offset, 0))
            screen.blit(mountain_img, (0 - bg_scroll * .6 + offset, SCREEN_HEIGHT - mountain_img.get_height() - 300))
            screen.blit(pine1_img, (0 - bg_scroll * .7 + offset, SCREEN_HEIGHT - pine1_img.get_height() - 150))
            screen.blit(pine2_img, (0 - bg_scroll * .8 + offset, SCREEN_HEIGHT - pine2_img.get_height()))

    def draw(self, screen_scroll):
        """Draws blocks to screen"""
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])

