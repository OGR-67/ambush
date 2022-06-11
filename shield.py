import pygame
from support import import_folder

class Shield(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.frame_index = 0
        self.frames = self.import_shield_assets()
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=self.player.rect.center)
        self.animation_speed = 1
    
    def import_shield_assets(self):
        path = "graphics/Shield"
        return import_folder(path, "Shield")
    
    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
    
    def stick_to_char(self):
        self.rect = self.image.get_rect(center=self.player.rect.center)
    
    def update(self):
        self.animate()
        self.stick_to_char()