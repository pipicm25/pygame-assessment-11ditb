from classes.sprite import Sprite
import pygame

IMAGE_SCALE = (100, 100)

# Extends custom sprite class
class Enemy(Sprite):
    def __init__(self, x, y, img):
        self.move_cooldown = 0 # Move cooldown
        self.shoot_cooldown = 0 # Shoot cooldown
        self.dead = False
        self.damage_per_bullet = 10
        self.x = x
        self.y = y
        
        img = pygame.transform.scale(img, IMAGE_SCALE)
        super().__init__(img, x, y) # Run sprite initialisation code
        
        
    # Run every frame
    def update(self) -> None:
        self.move_cooldown += 1
        self.shoot_cooldown += 1
        if self.move_cooldown >= 20:
            # Move and reset cooldown
            self.move(self.x, self.y + 10)
            self.move_cooldown = 0
            