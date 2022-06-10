import pygame

class Score():
    def __init__(self):
        self.score = 0
        self.get_best_score()
        
        self.font_size = 25
        self.font_left = 550
        self.font_top = 50
        self.font = pygame.font.Font("alagard.ttf", self.font_size)

    def get_best_score(self):
        with open("best_score.txt", "r") as f:
            self.best_score = int(f.read())
    
    def blit_score(self, screen):
        """Blit score on screen surface"""
        self.score_surf = pygame.font.Font.render(self.font, f"Your score: {self.score}", False, "white")
        self.best_score_surf = pygame.font.Font.render(self.font, f"Best score: {self.best_score}", False, "white")
        self.score_rect = self.score_surf.get_rect(topleft=(self.font_left, self.font_top))
        self.best_score_rect = self.score_surf.get_rect(bottomleft=self.score_rect.topleft)
        screen.blit(self.score_surf, self.score_rect)
        screen.blit(self.best_score_surf, self.best_score_rect)
    
    def set_score(self, difficulty, max_difficulty):
        self.score += int(100 * (max_difficulty / difficulty))

score = Score()
