import pygame
from support import import_folder

class Heart(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        topleft_coord = (10, 10)
        self.frame_index = 0
        self.frames = self.import_heart_assests()
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft=topleft_coord)
        
    def import_heart_assests(self):
        path = "graphics/Heart"
        asset = "Heart"
        return import_folder(path, asset)


heart = Heart()
    