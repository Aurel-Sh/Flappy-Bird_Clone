import pygame

class Score:
    def __init__(self, x: int, y: int, font: pygame.font.Font, text_col: tuple):
        self.count = 0
        self.x = x
        self.y = y
        self.font = font
        self.text_col = text_col
        self.images = {}
        try:
            for i in range(10):
                img = pygame.image.load(f'resources/Numbers/{i}.png')
                self.images.add = img
            self.image = self.images[0]
        except:
            pass
    
    def update(self):
        self.count += 1
        pass