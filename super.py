import pygame
from support import import_folder
from os import walk

class ChargedChar(pygame.sprite.Sprite):
    def __init__(self, player):
       super().__init__()
       self.player = player
       self.frame_index = 0
       self.frames = self.import_sprite_assets()
       self.image = self.frames[self.frame_index]
       self.rect = self.image.get_rect(center=self.player.rect.center)
       self.animation_speed = 0.40 
       
    def import_sprite_assets(self):
        path = "graphics/Charged"
        return import_folder(path, "Charged")
    
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


class ChargedBar(pygame.sprite.Sprite):
    def __init__(self, charge_bar):
       super().__init__()
       self.charge_bar = charge_bar
       self.frame_index = 0
       self.frames = self.import_sprite_assets()
       self.image = self.frames[self.frame_index]
       self.rect = self.image.get_rect(center=self.charge_bar.center)
       self.animation_speed = 0.6
       
    def import_sprite_assets(self):
        path = "graphics/Charged_bar"
        return import_folder(path, "Charged_bar")
    
    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
    
    def update(self):
        self.animate()


class SuperAttack(pygame.sprite.Sprite):
    def __init__(self, is_going_right, player_bottomleft, player_bottomright):
        super().__init__()
        self.load_attack_assets()
        self.frame_index = 0
        self.animation_speed = 0.4
        self.is_going_right = is_going_right
        
        self.image = self.frames[self.frame_index]
        self.get_rect(player_bottomleft, player_bottomright)

        self.is_over = False
        self.speed = 4
    
    def get_rect(self, player_bottomleft, player_bottomright):
        shift_x = 120
        shift_y = 120
        if self.is_going_right:
            self.rect = self.image.get_rect(bottomleft=player_bottomright)
            self.rect.x -= shift_x
        else:
            self.rect = self.image.get_rect(bottomright=player_bottomleft)
            self.rect.x += shift_x
        self.rect.y += shift_y
        
    def animate(self):
        self.frame_index += self.animation_speed
        self.image = self.frames[int(self.frame_index)]
        if not self.is_going_right: self.image = pygame.transform.flip(self.image, True, False)
        if self.frame_index > len(self.frames) - 1: 
            self.frame_index = 0
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

