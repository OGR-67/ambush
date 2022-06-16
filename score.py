import pygame
from settings import settings
from sprite_group import groups

class Score():
    def __init__(self):
        """Set the score to 0, get best_score from file, set position on screen"""
        self.score = 0
        self.get_best_score()
        self.font = settings.font
        self.set_score_surface()
        self.set_best_score_surface()
        self.set_score_rect()
        self.set_best_score_rect()

    def get_best_score(self):
        """Create best_score attribute and asign to it the value of the file best_score.txt"""
        with open("best_score.txt", "r") as f:
            self.best_score = int(f.read())

    def save_best_score(self):
        """Save current best_score to the file best_score.txt"""
        with open("best_score.txt", "w") as f:
                best_score_str = str(score.best_score)
                f.write(best_score_str)

    def set_score(self):
        """Increment score value each frames.
        Score increments faster when the difficulty increases.
        Score is frozen when player is dying."""
        if not groups["player"].sprite.is_dying:
            max_difficulty = settings.max_difficulty
            difficulty = settings.difficulty
            self.score += int(
                100 * (max_difficulty / difficulty)
                )

    def set_score_surface(self):
        """Create score surface."""
        self.score_surf = pygame.font.Font.render(
            settings.font, f"Your score: {self.score}", False, "white"
            )

    def set_best_score_surface(self):
        """Create best score surface."""
        self.best_score_surf = pygame.font.Font.render(
            settings.font, f"Best score: {self.best_score}", False, "white"
            )

    def set_score_rect(self):
        """Create score rect object."""
        self.score_rect = self.score_surf.get_rect(
            topleft=settings.score_position_coordinates
            )

    def set_best_score_rect(self):
        """Create best score rect object."""
        self.best_score_rect = self.best_score_surf.get_rect(
            bottomleft=self.score_rect.topleft
            )

    def reset_score(self):
        """Store current score to user_score and reset score to 0."""
        self.user_score = self.score
        self.score = 0

    def check_best_score(self):
        """Overwrite the best score if user_score is greater."""
        if self.user_score > self.best_score:
            self.best_score = self.user_score

    def blit_score(self):
        """Blit score and best score on screen surface"""
        settings.screen.blit(self.score_surf, self.score_rect)
        settings.screen.blit(self.best_score_surf, self.best_score_rect)

    def display_scores(self):
        """Set the scores and display them to the screen"""
        self.set_score()
        self.set_score_surface()
        self.set_best_score_surface()
        self.blit_score()

score = Score()
