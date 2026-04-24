import pygame

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = []
        self.index: int = 0
        self.counter: int = 0
        for num in range(1, 4):
            img = pygame.image.load(f'resources/imgs/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect() # create rect from boundaries of image
        self.rect.center = (x, y)
        self.vel: int = 0
        self.clicked: bool = False
        self.flying: bool = False
        self.game_over: bool = False
        self.die_sound = pygame.mixer.Sound('resources/audio/die.wav')
        self.hit_sound = pygame.mixer.Sound('resources/audio/hit.wav')
        self.wing_sound =  pygame.mixer.Sound('resources/audio/wing.wav')
        self.die_sound_played = False
        self.hit_sound_played = False
        

    def reset(self, screen_height: int):
        self.rect.x = 100
        self.rect.y = screen_height // 2
        self.game_over = False
        self.flying = False
        self.die_sound_played = False
        self.hit_sound_played = False
    
    def set_is_flying(self, is_flying):
        self.flying = is_flying
    
    def set_game_over(self, game_over):
        self.game_over = game_over

    def play_hit_sound(self):
        if not self.hit_sound_played:
            self.hit_sound.play()
        self.hit_sound_played = True

    def play_die_sound(self):
        if not self.die_sound_played:
            self.die_sound.play()
        self.die_sound_played = True

    def update(self):
        if not self.game_over:
            # animation
            self.counter += 1
            flap_cooldown = 5
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
                self.image = self.images[self.index]

            # rotation
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
            self.rect = self.image.get_rect(center=self.rect.center)
        else:
            self.image = self.images[1]
            self.image = pygame.transform.rotate(self.images[self.index], -45)
            self.rect = self.image.get_rect(center=self.rect.center)

        if self.flying:
            # gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += self.vel
            
            # jump 
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
                if self.clicked and not self.game_over:
                    self.wing_sound.play()
            if pygame.mouse.get_pressed()[0] == 0 :
                self.clicked = False
        else:
            self.image = self.images[0]
            self.image = pygame.transform.rotate(self.images[self.index], 0)
            self.rect = self.image.get_rect(center=self.rect.center)

        