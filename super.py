import pygame
from support import import_folder
from os import walk


class SuperAttack(pygame.sprite.Sprite):
    def __init__(self, is_going_right, bottomleft, bottomright):
        super().__init__()
        self.load_attack_assets()
        self.frame_index = 0
        self.animation_speed = 0.4
        self.is_going_right = is_going_right
        
        self.image = self.frames[self.frame_index]
        self.get_rect(bottomleft, bottomright)

        self.is_over = False
        
        self.speed = 4
    
    def get_rect(self, bottomleft, bottomright):
        if self.is_going_right:
            self.rect = self.image.get_rect(bottomleft=bottomright)
        else:
            self.rect = self.image.get_rect(bottomright=bottomleft)
        
    def animate(self):
        self.frame_index += self.animation_speed
        self.image = self.frames[int(self.frame_index)]
        if not self.is_going_right: self.image = pygame.transform.flip(self.image, True, False)
        if self.frame_index >= len(self.frames) - 1: 
            self.is_over = True
            self.kill()
    
    def move(self):
        if self.is_going_right:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed
    
    def load_attack_assets(self):
        path = "graphics/Super"
        frames = import_folder(path, "Super")
        self.frames = frames
        
    def update(self):
        if not self.is_over:
            self.move()
            self.animate()
        
# for _, __, image_file in walk("graphics/Super", True):
#     print(len(image_file))
#     image_file = sorted(image_file)
#     for image in image_file:
#             full_path = f"graphics/Super/{image}"
#             print(full_path)