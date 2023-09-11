from classes.sprite import Sprite
import pygame

BULLET_SCALE = (75, 75)
BULLET_SPEED = 6

# Extends sprite class
class Bullet(Sprite):
    def __init__(self, image, coordinates: tuple):
        # Scale and rotate bullet image
        image = pygame.transform.scale(image, BULLET_SCALE)
        image = pygame.transform.rotate(image, 90)
        super().__init__(image, coordinates[0], coordinates[1]) # Run sprite initialisation
    
    
    def update(self):
        self.move(self.x, self.y - BULLET_SPEED)
        
            