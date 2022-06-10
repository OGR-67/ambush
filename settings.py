import pygame

pygame.init()

class Settings:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 400
        self.screen_size = (self.screen_width, self.screen_height)
        self.floor = 300

        self.game_active = False
        self.game_started = False

        self.max_difficulty = 200
        self.start_difficulty = 2000
        self.difficulty = self.start_difficulty
        self.score = 0
        self.user_score = 0
        
    def set_difficulty(self):
        if self.difficulty > self.max_difficulty:
            self.difficulty -= 1
        
settings = Settings()
