import pygame

from random import choice
from settings import settings
from support import import_folder

mob_group = pygame.sprite.Group()


class Mob(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        # Spawn
        mob_types = ["demon", "lizard", "jinn"]
        self.type = str(choice(mob_types))
        self.spawn_choice = choice([1, -1])
        self.moving_right = True if self.spawn_choice == 1 else False
        
        # Animate
        self.frame_index = 0
        self.animation_speed = 0.10
        self.status = "Walk"
        self.assets = mob_assets.assets[self.type]
        self.animate()
        
        # Attribute
        self.hp = 1
        self.spawn()
        
        # When hit
        self.is_invincible = False
        self.start_point_x = 0
        
    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index > len(self.assets[self.status]):
            self.frame_index = 0
        self.image = self.assets[self.status][int(self.frame_index)]
        if not self.moving_right:
            self.image = pygame.transform.flip(self.image, True, False)
    
    def spawn(self):
        """Create a mob sprite, placing it acording top spawn_choice result,
        and add it to the mob group"""
        
        rect_bottom = settings.floor
        
        match self.type:
            case "demon":
                self.speed = 2
                self.hp = 2
            case "lizard": self.speed = 4
            case "jinn": self.speed = 3

        if self.type == "jinn": rect_bottom -= 50

        if self.spawn_choice == -1:
            self.rect = self.image.get_rect(midbottom=(settings.screen_width-30, rect_bottom))
        else:
            self.rect = self.image.get_rect(midbottom=(30, rect_bottom))
        mob_group.add(self)

    def move(self):
        """Move Mob to the opposite side of the screen"""
        
        if self.is_invincible:
            self.status = "Hurt"
            self.rect.x -= self.speed * self.spawn_choice
            if self.rect.x == self.start_point_x - (30 * self.spawn_choice):
                self.is_invincible = False
                self.status = "Walk"
        else: self.rect.x += self.speed * self.spawn_choice
        
        if self.rect.right <= 0 or self.rect.left >= settings.screen_width:
            mob_group.remove(self)
        
    def update(self, screen):
        mob_group.draw(screen)
        self.move()
        self.animate()

class MobAnimation:
    def __init__(self):
        self.assets = {
            "demon": {
                "Death": [],
                "Walk": [],
                "Hurt": []
                    },
            "jinn": {
                "Death": [],
                "Walk": [],
                "Hurt": []
                    },
                "lizard": {
                    "Death": [],
                    "Walk": [],
                    "Hurt": []
                    },
            }
        self.import_mobs_assets()

            
    def import_mobs_assets(self):
        path = "graphics/Mobs/"
        for mob in self.assets.keys():
            new_path = f"{path}{mob}/"  
            for animation in self.assets[mob].keys():
                fullpath = f"{new_path}{animation}"
                self.assets[mob][animation] = import_folder(fullpath, mob)

mob_assets = MobAnimation()
