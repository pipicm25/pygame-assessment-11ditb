import pygame

# Sprite extends pygame Sprite
class Sprite(pygame.sprite.Sprite):
    def __init__(self, image, startx: float, starty: float):
        super().__init__() # Runs the pygame sprite initialisation code
        
        self.x = startx
        self.y = starty
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = [startx, starty] 
    
    
    def move(self, x, y) -> None:
        self.rect.center = [x, y]
        self.x = x
        self.y = y
    
    
    def swap_image(self, image) -> None:
        self.image = image 
    
    
    def draw(self, screen) -> None: 
        screen.blit(self.image, self.rect) 