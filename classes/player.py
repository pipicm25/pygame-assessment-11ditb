import pygame
from classes.sprite import Sprite
        
RIGHT_X_BORDER = 800
LEFT_X_BORDER = 0
MOVE_SPEED = 4
        
# Player extends sprite class
class Player(Sprite):
    def __init__(self, x: float, y: float, image):
        self.cooldown = 0 
        self.move_right = False
        self.move_left = False
        self.move_per_frame = 0
        self.health = 100
        self.score = 0
        super().__init__(image, x, y) # Run sprite initialisation code
        
        
    # Run every tick
    def update(self, events):
        self.move(self.x + self.move_per_frame, self.y)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.move_per_frame += MOVE_SPEED
                if event.key == pygame.K_a:
                    self.move_per_frame -= MOVE_SPEED
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d or event.key == pygame.K_a:
                    self.move_per_frame = 0
        if self.x > RIGHT_X_BORDER: 
            self.move(LEFT_X_BORDER, self.y)
        elif self.x < LEFT_X_BORDER: 
            self.move(RIGHT_X_BORDER, self.y)
    
        