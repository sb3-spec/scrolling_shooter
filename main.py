import pygame
import os
pygame.init()
Sprite = pygame.sprite.Sprite

"""Setting up the game window"""
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = int(SCREEN_WIDTH * .8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
display = pygame.display
display.set_caption("2D Shooter")

clock = pygame.time.Clock()
FPS = 60

# define player variables

GRAVITY = .75

BG = (144, 201, 120)  # Background colors
RED = (255, 0, 0)

def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))

moving_left = False
moving_right = False

class Character(Sprite):
    """Basic class for the hero, serves as a blueprint for our characters"""
    def __init__(self, char_type, x, y, scale, speed=10):
        Sprite.__init__(self)

        self.speed = speed
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
        animation_types = ["Idle", "Running", "Jumping"]

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

    def move(self, moving_left, moving_right):
        dx = 0
        dy = 0

        if moving_left:
            dx = -self.speed
            self.flip = True
        if moving_right:
            dx = self.speed
            self.flip = False
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
                self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        flipped = pygame.transform.flip(self.image, self.flip, False)
        screen.blit(flipped, self.rect)


player = Character("player", 200, 600, 2)  

"""Game loop that is checking for user input"""
running = True
while running:

    clock.tick(FPS)
    draw_bg()
    player.update_animation()
    player.draw()  # draws the player's model to the screen
    player.move(moving_left, moving_right)

    # update player actions
    if player.alive:
        if moving_left or moving_right:
            player.update_action(1) # 1 is running
        elif player.in_air:
            player.update_action(2)
        else:
            player.update_action(0) # 0 is idle

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # keyboard button press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                moving_right = True
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                moving_left = True
            elif event.key == pygame.K_SPACE and player.alive:
                player.jump = True
            elif event.key == pygame.K_ESCAPE:
                running = False

        # keyboard button release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                moving_right = False
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                moving_left = False
            elif event.key == pygame.K_SPACE:
                player.jump = False

    display.update()  # Refreshes the screen


pygame.quit()