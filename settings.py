import pygame

pygame.init()

class Settings:
    def __init__(self):
        # screen
        self.screen_width = 800
        self.screen_height = 400
        self.screen_size = (self.screen_width, self.screen_height)
        # floor
        self.floor = 300
        # game state
        self.game_active = False
        self.game_started = False
        # difficulty
        self.max_difficulty = 200
        self.start_difficulty = 2000
        self.difficulty = self.start_difficulty
        # score
        self.score = 0
        self.user_score = 0
        # Sounds
        self.player_attack = pygame.mixer.Sound("sounds/audio_effects/Knight/attack.wav")
        self.player_death = pygame.mixer.Sound("sounds/audio_effects/Knight/death.wav")
        self.player_heavy_attack = pygame.mixer.Sound("sounds/audio_effects/Knight/heavyattack.wav")
        self.player_hit = pygame.mixer.Sound("sounds/audio_effects/Knight/hit.wav")
        self.player_jump = pygame.mixer.Sound("sounds/audio_effects/Knight/jump.wav")
        self.shockwave = pygame.mixer.Sound("sounds/audio_effects/shockwave.wav")
        self.shield = pygame.mixer.Sound("sounds/audio_effects/shield.wav")
        self.mob_hit = pygame.mixer.Sound("sounds/audio_effects/Mob/hit.wav")
        self.mob_death = pygame.mixer.Sound("sounds/audio_effects/Mob/death.wav")
        
    def scale_difficulty(self):
        if self.difficulty > self.max_difficulty:
            self.difficulty -= 1
            
    def reset(self):
        self.difficulty = settings.start_difficulty
        
settings = Settings()
