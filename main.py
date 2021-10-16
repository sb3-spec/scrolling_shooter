import pygame
from pygame import mixer
import pickle

pygame.init()
mixer.init()

Sprite = pygame.sprite.Sprite

from world import World
from settings import MAX_LEVELS, screen, SCREEN_HEIGHT, SCREEN_WIDTH, screen_scroll, bg_scroll
from button import Button

"""Setting up the game window"""

display = pygame.display
display.set_caption("2D Shooter")

clock = pygame.time.Clock()
FPS = 80

# game variables
ROWS = 16
COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 21
level = 1
start_game = False
# define player variables
moving_left = False
moving_right = False
shooting = False
grenade = False
grenade_thrown = False


# define font
font = pygame.font.SysFont('Futura', 30)

# load in button images
start_btn_img = pygame.image.load("./assets/Buttons/start_btn.png")
exit_btn_img = pygame.image.load("./assets/Buttons/exit_btn.png")
restart_btn_img = pygame.image.load("./assets/Buttons/restart_btn.png")

# load in music and sounds
mixer.music.load('./assets/Audio/audio_music2.mp3')
mixer.music.set_volume(.01)
mixer.music.play(-1, 0.0, 5000)
jump_fx = mixer.Sound("./assets/Audio/audio_jump.wav")
jump_fx.set_volume(.5)
grenade_fx = mixer.Sound("./assets/Audio/audio_grenade.wav")
grenade_fx.set_volume(.5)
shot_fx = mixer.Sound("./assets/Audio/audio_shot.wav")
shot_fx.set_volume(.5)



def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def reset_level():
    """Funtion to reset level"""
    enemy_group.empty()
    bullet_group.empty()
    grenade_group.empty()
    explosion_group.empty()
    item_box_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()
    bullet_group.empty()
    # create empty world data
    data = []
    pickle_in = open(f'./level_data/level{level}_data', 'rb')
    data = pickle.load(pickle_in)

    return data

# color definitions
BG = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# various groups to handle different sprites
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
box_group = pygame.sprite.Group()


# create buttons
start_btn = Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 150, start_btn_img, 1)
exit_btn = Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 50, exit_btn_img, 1)
restart_btn = Button(SCREEN_WIDTH // 2 - 115, SCREEN_HEIGHT // 2 - 50, restart_btn_img, 2)




# create empty tile list
world_data = []
pickle_in = open(f'./level_data/level{level}_data', 'rb')
world_data = pickle.load(pickle_in)

world = World()
player, health_bar = world.process_data(world_data, enemy_group, item_box_group, water_group, decoration_group, exit_group, box_group)

"""Game loop that is checking for user input"""
running = True
while running:

    clock.tick(FPS)

    if not start_game: # check if in main menu or not
        # in main menu
        screen.fill(BG)
        if start_btn.draw(screen):
            start_game = True
        if exit_btn.draw(screen):
            running = False
    else:   
        # update background
        world.draw_bg(bg_scroll)
        
        # draw world map
        world.draw(screen_scroll)

        # show player health
        health_bar.draw(player.health, screen)
        player.update()
        player.draw()  # draws the player's model to the screen
        screen_scroll, level_complete = player.move(moving_left, moving_right, world, bg_scroll, water_group, exit_group, box_group)
        bg_scroll -= screen_scroll

        # check if player has completed level
        if level_complete:
            level += 1
            bg_scroll = 0
            world_data = reset_level()
            if level <= MAX_LEVELS:
                world = World()
                player, health_bar = world.process_data(world_data, enemy_group, item_box_group, water_group, decoration_group, exit_group)

        # draw ammo count
        draw_text(f"AMMO: {player.ammo}", font, WHITE, 10, 35 )

        # draw grenade count
        draw_text("GRENADES: ", font, WHITE, 10, 60 )
        grenade_img = pygame.image.load("./assets/Icons/grenade.png")
        for i in range(player.grenades):
            screen.blit(grenade_img, (135 + (i * 15), 63))

        # checking if grenades have detonated
        for grenade_ in grenade_group:
            explosion = grenade_.handle_explosion(player, enemy_group, grenade_fx)
            if explosion:
                explosion_group.add(explosion)

        # update destructible boxes
        for box in box_group:
            explosion = box.handle_explosion(grenade_fx, enemy_group, box_group, player)
            if explosion:
                explosion_group.add(explosion)

        # update enemies

        for enemy in enemy_group:
            enemy.ai(bullet_group, player, grenade_group, world, screen_scroll, bg_scroll, water_group, exit_group, shot_fx, box_group)
            enemy.update()
            enemy.draw()
        # update bullets
        bullet_group.update(player, enemy_group, world, screen_scroll, box_group)
        bullet_group.draw(screen) 
        # update grenades
        grenade_group.update(world, screen_scroll)
        grenade_group.draw(screen)
        # update explosions
        explosion_group.update(screen_scroll)
        explosion_group.draw(screen)
        # update item boxes
        item_box_group.update(player, screen_scroll)
        item_box_group.draw(screen)
        # update water
        water_group.update(screen_scroll)
        water_group.draw(screen)
        # updates decorations
        decoration_group.update(screen_scroll)
        decoration_group.draw(screen)
        # # update explosive boxes
        box_group.update(screen_scroll)
        box_group.draw(screen)




        # update player actions
        if player.alive:
            if shooting:
                player.shoot(bullet_group, shot_fx)
            elif grenade and not grenade_thrown and player.grenades > 0:
                # throw grenades
                grenade_thrown = True
                grenade_group.add(player.grenade())
            if moving_left or moving_right:
                player.update_action(1) # 1 is running
            elif player.in_air:
                player.update_action(2)       
            else:
                player.update_action(0) # 0 is idle
        else:
            screen_scroll = 0
            if restart_btn.draw(screen):
                bg_scroll = 0
                world_data = reset_level()
                world = World()
                player, health_bar = world.process_data(world_data, enemy_group, item_box_group, water_group, decoration_group, exit_group, box_group)

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
                jump_fx.play()
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