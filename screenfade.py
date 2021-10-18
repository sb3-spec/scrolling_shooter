import pygame
from settings import SCREEN_WIDTH, screen, SCREEN_HEIGHT

class ScreenFade():
    def __init__(self, direction, color, speed):
        self.direction = direction
        self.color = color
        self.speed = speed
        self.fade_counter = 0
        
    def fade(self):
        self.fade_counter += self.speed
        
        if self.direction == 1: # whole screen fade
            # horizontal fade
            pygame.draw.rect(screen, self.color, (0 - self.fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
            pygame.draw.rect(screen, self.color, (SCREEN_WIDTH // 2 + self.fade_counter, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT))
            
            # vertical fade
            pygame.draw.rect(screen, self.color, (0, 0 - self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
            pygame.draw.rect(screen, self.color, (0, SCREEN_HEIGHT // 2 + self.fade_counter, SCREEN_WIDTH, SCREEN_HEIGHT // 2))
            
        if self.direction == 2: # vertical screen fade
            pygame.draw.rect(screen, self.color, (0, 0, SCREEN_WIDTH, 0 + self.fade_counter))

        return self.fade_counter > SCREEN_HEIGHT
        