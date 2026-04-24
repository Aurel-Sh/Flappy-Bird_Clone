import pygame
from pygame.locals import *
from classes.bird import Bird
from classes.pipe import Pipe
from classes.button import Button
from utils import draw_txt, reset_game
import random


def main():
    pygame.init()
    pygame.mixer.init()

    clock = pygame.time.Clock()
    fps: int = 60

    # screen dimensions
    screen_width: int = 864
    screen_height: int = 936
    start: bool = False
    game_over: bool = False
    pipe_gap: int = 150
    pipe_frequency: int = 1500 # milliseconds
    last_pipe = pygame.time.get_ticks()
    score: int = 0
    passed_pipe: bool = False
    font = pygame.font.SysFont('Bauhaus 93', 70)
    font_small = pygame.font.SysFont('Bauhaus 93', 40)
    white = (255, 255, 255)

    screen = pygame.display.set_mode((screen_width, screen_height))
    # window title
    pygame.display.set_caption("Flappy Bird Clone")
    
    # load images
 
    bg = pygame.image.load(f'resources/imgs/backgrounds/Background0.png')
    ground = pygame.image.load('resources/imgs/ground.png')
    restart_button = pygame.image.load('resources/imgs/restart.png')

    # groups
    bird_group = pygame.sprite.Group()
    pipe_group = pygame.sprite.Group()

    flappy = Bird(100, screen_height // 2)
    bird_group.add(flappy)



    # variables
    ground_scroll: int = 0
    bg_scroll: int = 0
    scroll_speed: int = 4 # 4 pixels per iteration
    
    # instantiate restart button
    button = Button(screen_width // 2 - 50, screen_height // 2 - 100, restart_button)



    # main game loop
    running = True
    while running:

        clock.tick(fps)
        screen.blit(bg, (bg_scroll, 0)) # draw background from top-left corner
        screen.blit(bg, (bg_scroll + bg.get_width(), 0))


        # draw flappy
        bird_group.draw(screen)
        bird_group.update()

        # draw pipe
        pipe_group.draw(screen)
        # draw and scroll ground
        screen.blit(ground, (ground_scroll, screen_height - ground.get_height())) # order of blit is important

        # check score
        if len(pipe_group) > 0:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left \
                and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right \
                and passed_pipe == False:
                passed_pipe = True
            if passed_pipe == True:
                if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                    score += 1
                    pygame.mixer.Sound('resources/audio/point.wav').play()
                    passed_pipe = False


        draw_txt(str(score), font, white, screen_width // 2, 20, screen)

        # check pipe collision
        if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
            game_over = True
            flappy.set_game_over(game_over)
            flappy.play_hit_sound()
            flappy.play_die_sound()



        # check ground collision:
        if flappy.rect.bottom >= screen_height - ground.get_height():
            game_over = True
            flappy.set_game_over(game_over)
            flappy.play_hit_sound()

            
        if not game_over:
            if start:
                # generate new pipes
                time_now = pygame.time.get_ticks()
                if time_now - last_pipe > pipe_frequency:
                    pipe_height = random.randint(-75, 75)
                    btm_pipe = Pipe(screen_width + 10, screen_height//2 + pipe_height, -1)
                    top_pipe = Pipe(screen_width + 10, screen_height//2 + pipe_height, 1)
                    pipe_group.add(top_pipe)
                    pipe_group.add(btm_pipe)
                    last_pipe = time_now
                pipe_group.update()


            ground_scroll -= scroll_speed
            bg_scroll -= scroll_speed / 4

            if abs(ground_scroll) >= ground.get_width() - bg.get_width(): # if ground is out of the screen, reset scroll position (ground scroll) <= ground.get_width() - bg.get_width():
                ground_scroll = 0
            if abs(bg_scroll) > bg.get_width():
                bg_scroll = 0

        # check for game over and restart
        if game_over:
                # restart button instance
                clicked = button.draw(screen)
                if clicked:
                    score = reset_game(pipe_group, flappy, screen_height)
                    game_over = False
                    start = False


        for event in pygame.event.get(): # event handler to manage quitting
            if event.type == QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and start == False and game_over == False:
                start = True
                flappy.set_is_flying(start)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
