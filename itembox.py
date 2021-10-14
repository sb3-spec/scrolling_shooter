import pygame

from grenade import TILE_SIZE
Sprite = pygame.sprite.Sprite
#pickup boxes
ammo_box_img = pygame.image.load("./assets/Icons/ammo_box.png")
grenade_box_img = pygame.image.load("./assets/Icons/grenade_box.png")
health_box_img = pygame.image.load("./assets/Icons/health_box.png")
item_boxes = {
    'Health' : health_box_img,
    "Grenade" : grenade_box_img,
    "Ammo" : ammo_box_img
}

class ItemBox(Sprite):
    """Class for the item boxes objects"""
    def __init__(self, item_type, x, y) -> None:   
        Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
    
    def update(self, player, screen_scroll):
        """Update method for item boxes"""
        if pygame.sprite.collide_rect(self, player):
            if self.item_type == "Health":
                player.health += 50
            elif self.item_type == "Ammo":
                player.ammo = player.start_ammo
            elif self.item_type == "Grenade":
                player.grenades += 5
            
            self.kill()
        # account for scroll
        self.rect.x += screen_scroll