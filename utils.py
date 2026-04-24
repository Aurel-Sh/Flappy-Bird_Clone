import pygame
def draw_txt(text: str, font: pygame.font.Font, text_col: tuple, x: int, y: int, screen: pygame.Surface):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def reset_game(pipe_group, flappy, screen_height):
    pipe_group.empty()
    flappy.reset(screen_height)
    score = 0
    return  score