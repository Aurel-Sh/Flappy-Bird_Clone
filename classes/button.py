import pygame

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    
    def draw(self, screen: pygame.Surface):
        clicked: bool = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
        # draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return clicked