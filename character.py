import pygame
import os
from bullet import Bullet
Sprite = pygame.sprite.Sprite

GRAVITY = .75

class Character(Sprite):
    """Basic class for the hero, serves as a blueprint for our characters"""
    def __init__(self, screen, char_type, x, y, scale, ammo, bullet_group, speed=5):
        Sprite.__init__(self)
        self.screen = screen
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
        self.jump = False
        self.in_air = True
        self.alive = True
        self.vel_y = 0
        self.update_time = pygame.time.get_ticks()
        
        
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

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.update_animation()
        self.check_alive()
        # update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
    
    def move(self, moving_left, moving_right):
        dx = 0
        dy = 0

        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        if self.jump and not self.in_air:
            self.vel_y = -11
            self.jump = False
            self.in_air = True
        

        # Apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy = self.vel_y

        #check collision with floor

        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False

        self.rect.x += dx
        self.rect.y += dy


    def shoot(self, bullet_group):
        """Method that creates bullet objects"""
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 40
            bullet = Bullet(self.rect.centerx + ((self.rect.size[0] / 2) * self.direction), self.rect.centery, self.direction, bullet_group)
            bullet_group.add(bullet)
            # reduces ammo
            self.ammo -= 1
            


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