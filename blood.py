import pygame
from support import import_folder

class Blood(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        center_coord = (35, 20)
        self.frame_index = 0
        self.animation_speed = 0.8
        self.frames = self.import_sprite_assets()
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=center_coord)
    
    def import_sprite_assets(self):
        path = "graphics/Blood"
        asset = "Blood"
        return import_folder(path, asset)
    
    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index > len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
    
    def update(self):
        self.animate()


blood = Blood()
        