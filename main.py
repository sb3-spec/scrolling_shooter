import pygame
pygame.init()
Sprite = pygame.sprite.Sprite
from character import Character

"""Setting up the game window"""
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = int(SCREEN_WIDTH * .8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
display = pygame.display
display.set_caption("2D Shooter")

clock = pygame.time.Clock()
FPS = 60

# define player variables



BG = (144, 201, 120)  # Background colors
RED = (255, 0, 0)

def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))

moving_left = False
moving_right = False

player = Character(screen, "player", 200, 600, 2)  

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