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
FPS = 80

# define player variables
moving_left = False
moving_right = False
shooting = False
grenade = False
grenade_thrown = False



BG = (0, 0, 0)  # Background colors
RED = (255, 0, 0)

def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 300), (SCREEN_WIDTH, 300))
 

# various groups to handle different sprites
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()

# Creating character instances

player = Character(screen, "player", 200, 600, 2, 20, bullet_group, 10)
enemy = Character(screen, "enemy", 400, 250, 2, 20, bullet_group, 0)
enemy.rect.bottom = 300

character_group = pygame.sprite.Group()



"""Game loop that is checking for user input"""
running = True
while running:

    clock.tick(FPS)
    draw_bg()
    player.update()
    player.draw()  # draws the player's model to the screen
    player.move(moving_left, moving_right)
    enemy.update()
    enemy.draw()

    
    # checking if grenades have detonated
    for grenade in grenade_group:
        explosion = grenade.handle_explosion()
        if explosion:
            explosion_group.add(explosion)


    # update and draw groups
    bullet_group.update(player, enemy)
    bullet_group.draw(screen) 
    grenade_group.update()
    grenade_group.draw(screen)
    explosion_group.update()
    explosion_group.draw(screen)




    # update player actions
    if player.alive:
        if shooting:
            player.shoot(bullet_group)
        elif grenade and not grenade_thrown:
            # throw grenades
            grenade_thrown = True
            if grenade and player.grenades > 0:
                grenade_group.add(player.grenade())
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
            elif event.key == pygame.K_SPACE or event.key == pygame.K_UP and player.alive:
                player.jump = True
            elif event.key == pygame.K_SPACE:
                shooting = True
            elif event.key == pygame.K_q:
                grenade = True
            elif event.key == pygame.K_ESCAPE:
                running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            shooting = True
        
        if event.type == pygame.MOUSEBUTTONUP:
            shooting = False
        
        # keyboard button release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                moving_right = False
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                moving_left = False
            elif event.key == pygame.K_SPACE:
                shooting = False
            elif event.key == pygame.K_q:
                grenade = False
                grenade_thrown = False
            elif event.key == pygame.K_SPACE:
                shooting = False


        

    display.update()  # Refreshes the screen


pygame.quit()