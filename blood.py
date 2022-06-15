import pygame
import utility_classes


class Blood(utility_classes.AnimatedSprite):
    def __init__(self):
        super().__init__("blood", "graphics", None)
        center_coord = (35, 20)
        self.animation_speed = 0.8
        self.image = self.frames[self.frame_index]
        self.rect.center = center_coord
    
    def update(self):
        self.animate()


blood = Blood()
        