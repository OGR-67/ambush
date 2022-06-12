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
        
    def scale_difficulty(self):
        if self.difficulty > self.max_difficulty:
            self.difficulty -= 1
            
    def reset(self):
        self.difficulty = settings.start_difficulty
        self.game_active =  False
        
settings = Settings()
