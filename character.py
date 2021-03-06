import pygame
import os
from bullet import Bullet
from grenade import Grenade
import random as r

from settings import SCREEN_HEIGHT, SCREEN_WIDTH, SCROLL_THRESH, TILE_SIZE, GRAVITY, screen, PINK

Sprite = pygame.sprite.Sprite

class Character(Sprite):
    """Basic class for the hero, serves as a blueprint for our characters"""
    def __init__(self, screen, char_type, x, y, scale, ammo, grenades, speed=5):
        Sprite.__init__(self)
        self.screen = screen
        self.walking_speed = speed
        self.running_speed = 1.5 * self.walking_speed
        self.grenades = grenades
        self.speed = speed
        self.start_ammo = ammo
        self.ammo = ammo
        self.direction = 1
        self.shoot_cooldown = 0
        self.health = 100
        self.max_health = self.health
        self.x = x
        self.y = y
        self.char_type = char_type
        self.flip = False
        self.action = 0
        self.frame_index = 0
        self.animation_list = []
        self.jump_speed = -15
        self.jump = False
        self.in_air = True
        self.alive = True
        self.vel_y = 0
        self.update_time = pygame.time.get_ticks()

        # ai specific variables
        self.move_counter = 0
        self.idling = False
        self.idling_counter = 0
        self.max_visible_length = 200
        self.visible_length = self.max_visible_length
        self.vision = pygame.Rect(0, 0, self.max_visible_length, 20)
        self.grenade_counter = 0
        
        
        # loading in all images
        animation_types = ["Idle", "Running", "Jumping", "Death"]

        for type in animation_types:
            # resets temporary image list
            temp_list = []
            # count number of files in the action folder
            num_of_frames = len(os.listdir(f'./assets/{self.char_type}/{type}'))

            for i in range(num_of_frames):
                img = pygame.image.load(f'./assets/{self.char_type}/{type}/{i}.png')
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)

            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.update_animation()
        self.check_alive()
        # update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
    
    def move(self, moving_left, moving_right, world, bg_scroll, water_group, exit_group, box_group):
        # reset movement variables
        screen_scroll = 0
        
        dx = 0
        dy = 0 
        
        if self.alive:
            if moving_left:
                dx = -self.speed
                self.flip = True
                self.direction = -1
            if moving_right:
                dx = self.speed
                self.flip = False
                self.direction = 1
                
            if self.jump and not self.in_air:
                self.vel_y = self.jump_speed
                self.jump = False
                self.in_air = True
        
        # Apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # check collision with non destroyable obstacles 
        for tile in world.obstacle_list:
            # check in x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                if self.char_type == "Enemy":
                    self.direction *= -1
                    self.move_counter = 0
            # check in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0: # check if jumping
                    self.vel_y = 0
                    dy = self.rect.top - tile[1].bottom
                elif self.vel_y >= 0: # check if falling
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom
        
        
        # checks collision with boxes
        for box in box_group:
            if box.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                if self.char_type == "Enemy":
                    self.direction *= -1
                    self.move_counter = 0
            if box.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0: # check if jumping
                    self.vel_y = 0
                    dy = self.rect.top - box.rect.bottom
                elif self.vel_y >= 0: # check if falling
                    self.vel_y = 0
                    self.in_air = False
                    dy = box.rect.top - self.rect.bottom

        # check if in contact with water
        if pygame.sprite.spritecollide(self, water_group, False):
            self.health = 0
        
        # check if player falls off map
        if self.rect.y > SCREEN_HEIGHT:
            self.health = 0

        # check for collision with exit
        level_complete = False
        if pygame.sprite.spritecollide(self, exit_group, False):
            level_complete = True
        # check if going off the edges of the screen
        if self.char_type == "player":
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0

        # update rectangle position      
        self.rect.x += dx
        self.rect.y += dy

        # update scroll based on player position
        
        if self.char_type == "player":
            if ((self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE))\
                or self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx
            
        return screen_scroll * 1.25, level_complete



    def shoot(self, bullet_group, shot_fx):
        """Method that creates bullet objects"""
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 15
            bullet = Bullet(self.rect.centerx + ((self.rect.size[0] * .75) * self.direction), self.rect.centery, self.direction, bullet_group)
            bullet_group.add(bullet)
            shot_fx.play()
            # reduces ammo
            self.ammo -= 1
    
    def ai(self, bullet_group, player, grenade_group, world, screen_scroll, bg_scroll, water_group, exit_group, shoot_fx, box_group):
        """function to handle enemy movement/awareness"""

        if self.alive and player.alive:
            if r.randint(1, 250) == 5 and not self.idling:
                self.idling = True
                self.update_action(0) # idle
                self.idling_counter = 100 # how long the ai is idle for
                
            # checks if ai view is obstructed
            tile_min_dist = 200
            box_min_dist = 200
            
            # checking non destructable tiles
            for tile in world.obstacle_list:
                if self.vision.colliderect(tile[1]):
                    dist_left = abs(tile[1].right - self.rect.left)
                    dist_right = abs(tile[1].left - self.rect.right)
                    tile_dist = min(dist_left, dist_right)
                    tile_min_dist = min(tile_min_dist, tile_dist)
            
            # checking destructibles boxes
            for box in box_group:
                if self.vision.colliderect(box.rect):
                    dist_left = abs(box.rect.right - self.rect.left)
                    dist_right = abs(box.rect.left - self.rect.right)
                    box_dist = min(dist_left, dist_right)
                    box_min_dist = min(box_dist, box_min_dist)
                    
            nearest_visible_obstacle_dist = min(box_min_dist, tile_min_dist)
            
            
            self.vision.width = nearest_visible_obstacle_dist
            
                
            # check if enemy sees the player
            if self.vision.colliderect(player.rect):
                self.update_action(0) # idling
                self.shoot(bullet_group, shoot_fx)
                nade = self.grenade()
                if nade:
                    grenade_group.add(nade)
                
                # TODO 
                # Enemy not shooting when seeing player
                
                
                
            else:
                if not self.idling:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right, world, bg_scroll, water_group, exit_group, box_group)
                    self.update_action(1) # run
                    self.move_counter += 1
                    
                    
                    
                    
                    if self.move_counter > TILE_SIZE * 2:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False
                        
        # update enemy vision
        self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)
        self.rect.x += screen_scroll

            




    def grenade(self):
            if self.grenades > 0 and self.alive:
                grenade = Grenade(self.rect.centerx + (.5 * self.rect.size[0] * self.direction), self.rect.top, self.direction)
                self.grenades -= 1
                return grenade
            return


    def update_animation(self):
        # Update animation
        ANIMATION_COOLDOWN = 100
        #update image depending on current time
        self.image = self.animation_list[self.action][self.frame_index]

        #check if enough time has passed since last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            if self.frame_index == len(self.animation_list[self.action]):
                if self.action != 3:
                    self.frame_index = 0
                else:
                    self.frame_index = len(self.animation_list[self.action]) - 1

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.update_action(3)
            self.alive = False

    def draw(self):
        flipped = pygame.transform.flip(self.image, self.flip, False)
        self.screen.blit(flipped, self.rect)