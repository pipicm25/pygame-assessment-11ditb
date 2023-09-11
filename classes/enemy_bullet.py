from classes.sprite import Sprite
import pygame

BULLET_SCALE = (50, 50)
BULLET_SPEED = 6

# Class extends EnemyBullet Class
class EnemyBullet(Sprite):
    def __init__(self, image, coordinates: tuple, host: Sprite):
        # Scale bullet image
        self.host = host
        image = pygame.transform.scale(image, BULLET_SCALE)
        super().__init__(image, coordinates[0], coordinates[1]) # Run sprite initialisation
        
    def update(self):
        self.move(self.x, self.y + BULLET_SPEED)