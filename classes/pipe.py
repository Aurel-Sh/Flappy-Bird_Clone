import pygame
import random
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position, pipe_gap=150):
        super().__init__()
        self.image = pygame.image.load('resources/imgs/pipe.png')
        self.rect = self.image.get_rect()
        # position 1 is top, position -1 is bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, position == 1)
            self.rect.bottomleft = (x, y - pipe_gap // 2)
        if position == -1:
            self.rect.topleft = (x, y + pipe_gap // 2)
    
    def update(self, scroll_speed: int = 4):
        self.rect.x -= scroll_speed # move pipes left
        if self.rect.right < 0 :
            self.kill() # remove pipe from memory once off screen
