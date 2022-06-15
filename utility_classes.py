from math import floor
import pygame
from support import import_folder
from sprite_group import groups


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, asset, path, dict):
        """init instance:
        asset: Sprite asset
        path: Relative path to the asset folder
        dict: Dictionary of animations. None if single animation
        - parameter created: animation_speed, frame_index, frames, image, rect
        - method created: animate"""
        self.get_animation_speed()
        self.get_frame_index()
        self.get_frames(asset, path, dict)
        self.get_rectangle()
        self._Sprite__g = {}
    
    def get_animation_speed(self):
        """Create animation_speed attribute:
        Default value: 0.15
        """
        self.animation_speed = 0.15
    
    def get_frame_index(self):
        """Create frame_index attribute:
        Default value: 0
        """
        self.frame_index = 0
    
    def get_frames(self, asset, path, dict):
        """Import sprite assests. Takes 3 parameters:
        - path: Path to asset's parent folder
        - asset: assets folder name
        - dict: dictionnary of animations name with empty lists. If only one animation, put None
        As a result, frames is created. Can be a list if dict is None or a dict of lists"""
        if dict == None:
            self.frames = import_folder(f"{path}/{asset}", asset)
            self.image = self.frames[0]
        else:
            self.frames = {}
            for key in dict.keys():
                self.status = key
                full_path = f"{path}/{asset}/{key}"
                self.frames[key] = import_folder(full_path, asset)
                if not self.direction_right:
                    for index, image in enumerate(self.frames[key]):
                        self.frames[key][index] = pygame.transform.flip(image, True, False)
            self.status = list(dict.keys())[0]
            self.image = self.frames[self.status][0]
                
    
    def animate(self):
        """Create/update image attribute based on current frame index"""
        if type(self.frames) == list:
            image_to_animate = self.frames
        else:
            image_to_animate = self.frames[self.status]
        self.frame_index += self.animation_speed
        index = floor(self.frame_index) 
        if index >= len(image_to_animate):
            index = self.frame_index = 0
        self.image = image_to_animate[index]
        
    def get_rectangle(self):
        """Create sprite rect and place it's top left corner
        to origin point (0, 0)"""
        self.rect = self.image.get_rect(topleft=(0,0))
    
    # def get_direction_right(self):
    #     """Set direction to right."""
    #     if self.direction_right is None:
    #         self.direction_right = True
    
    def flip_x_image_if_left(self, image):
        """Flips the image horizontally if direction_right is False."""
        if not self.direction_right:
            return pygame.transform.flip(image, True, False)
        

class HitboxSprite(pygame.sprite.Sprite):
    def __init__(self, size):
        """Create a new HitboxSprite object with an image surface of size
        'size' and a rect object placed at origin point of display surface."""
        super().__init__()
        self.get_image(size)
        self.get_rect()
        
    def get_image(self, size):
        """Create image surface of a given size"""
        self.image = pygame.Surface(size)
    
    def get_rect(self):
        """Create rect from image attribute"""
        self.rect = self.image.get_rect(topleft = (0,0))
     
from settings import settings

class Test(AnimatedSprite):
    def __init__(self):
        knight_animations_dict = {
                    "Attack": [],
                    "Run": [],
                    "Jump": [],
                    "Attack_Extra": [],
                    "Stand": [],
                    "Death": [],
                }
        super().__init__("Knight", "graphics", knight_animations_dict)
        
# class ParentTest(pygame.sprite.Sprite):
#     def __init__(self):
#         super().__init__()


# class Test(ParentTest):
#     def __init__(self):
#         super().__init__()

# a_group = pygame.sprite.GroupSingle()
# test = Test()
# a_group.add(test)
# print(a_group.sprites())
