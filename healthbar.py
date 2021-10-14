import pygame
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

class HealthBar():
    """Class for the healthbar objects"""
    def __init__(self, x, y, health, max_health) -> None:
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    def draw(self, health, screen):
        """Updates health bar to reflect current health"""
        self.health = health
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))