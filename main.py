import pygame
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

BG = (144, 201, 120)  # Background colors

moving_left = False
moving_right = False

class Character(Sprite):
    """Basic class for the hero, serves as a blueprint for our characters"""
    def __init__(self, x, y, scale, speed=10):
        Sprite.__init__(self)

        self.speed = speed
        self.x = x
        self.y = y

        img = pygame.image.load('assets/mario.png')
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self, moving_left, moving_right):
        dx = 0
        dy = 0

        if moving_left:
            dx = -self.speed
        if moving_right:
            dx = self.speed
        self.rect.x += dx
        self.rect.y += dy

    def draw(self):
        screen.blit(self.image, self.rect)

    def jump(self):
        dy = 5
        self.rect.y += dy

def draw_bg():
    screen.fill(BG)


hero = Character(200, 600, .05)  

"""Game loop that is checking for user input"""
running = True
while running:

    clock.tick(FPS)
    draw_bg()
    hero.draw()  # draws the hero's model to the screen
    hero.move(moving_left, moving_right)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # keyboard button press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                moving_right = True
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                moving_left = True
            elif event.key == pygame.K_ESCAPE:
                running = False

        # keyboard button release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                moving_right = False
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                moving_left = False

    display.update()  # Refreshes the screen


pygame.quit()