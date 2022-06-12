import pygame

from random import choice
from settings import settings
from support import import_folder


class Mob(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        # Spawn
        mob_types = ["demon", "lizard", "jinn", "lizard", "jinn"]
        self.type = str(choice(mob_types))
        self.spawn_choice = choice([1, -1])
        self.moving_right = True if self.spawn_choice == 1 else False
        
        # Animate
        self.spawn()
        self.hitbox_sprite.frame_index = 0
        self.animation_speed = 0.18
        self.assets = mob_assets.assets[self.type]
        self.animate()
        self.rect = self.image.get_rect(topleft=(settings.screen_width,0))
        
    def animate(self):
        self.hitbox_sprite.frame_index += self.animation_speed
        last_frame_index = len(self.assets[self.hitbox_sprite.status])
        if self.hitbox_sprite.frame_index > last_frame_index:
            if self.hitbox_sprite.status == "Death":
                self.hitbox_sprite.frame_index = 0
                self.kill()
                self.hitbox_sprite.kill()
            else:
                self.hitbox_sprite.frame_index = 0
        self.image = self.assets[self.hitbox_sprite.status][int(self.hitbox_sprite.frame_index)]
        if not self.moving_right:
            self.image = pygame.transform.flip(self.image, True, False)
    
    def spawn(self):        
        rect_bottom = settings.floor
        match self.type:
            case "demon":
                self.speed = 2
                size = (60, 85)
            case "lizard": 
                self.speed = 4
                size = (70, 45)
            case "jinn": 
                self.speed = 3
                size = (40, 70)
                rect_bottom -= 50
        self.hitbox_sprite = MobHitbox(size)
        if self.type == "demon": self.hitbox_sprite.hp = 2
        if self.spawn_choice == -1:
            self.hitbox_sprite.rect.midbottom = (settings.screen_width-30, rect_bottom)
        else: self.hitbox_sprite.rect.midbottom = (30, rect_bottom)
        mob_group.add(self)
        mob_hitbox_group.add(self.hitbox_sprite)
        
    def stick_asset_to_hibox(self):
        match self.type:
            case"demon":
                shift_y = 15
                shift_x = 30 * self.spawn_choice
            case"jinn":
                shift_y = 15
                shift_x = 10 * self.spawn_choice
            case"lizard":
                shift_y = 0
                shift_x = 0 * self.spawn_choice
        self.rect.centerx = self.hitbox_sprite.rect.centerx + shift_x
        self.rect.centery = self.hitbox_sprite.rect.top + shift_y        

    def move(self):
        """Move Mob to the opposite side of the screen"""
        offset_x = 30 * self.spawn_choice
        if self.hitbox_sprite.is_invincible:
            self.hitbox_sprite.status = "Hurt"
            self.hitbox_sprite.rect.x -= self.speed * self.spawn_choice
            if self.hitbox_sprite.rect.x == self.hitbox_sprite.start_point_x - offset_x:
                self.hitbox_sprite.is_invincible = False
                self.hitbox_sprite.status = "Walk"
        else: self.hitbox_sprite.rect.x += self.speed * self.spawn_choice
        
        if self.hitbox_sprite.rect.right <= -50 or \
        self.hitbox_sprite.rect.left >= settings.screen_width + 50:
            self.kill()
            self.hitbox_sprite.kill()
        
    def update(self, screen):
        if self.hitbox_sprite.status != "Death": self.move()
        if self.alive(): self.animate()
        self.stick_asset_to_hibox()
        mob_group.draw(screen)


class MobHitbox(pygame.sprite.Sprite):
    def __init__(self, size):
        super().__init__()
        starting_point = (0, 0)
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(midbottom=starting_point)
        
        self.hp = 1
        self.status = "Walk"
        self.is_invincible = False
        self.start_point_x = 0


class MobAnimation:
    def __init__(self):
        self.assets = {
            "demon": {"Death": [], "Walk": [], "Hurt": []},
            "jinn": {"Death": [], "Walk": [], "Hurt": []},
                "lizard": {"Death": [], "Walk": [], "Hurt": []},
            }
        self.import_mobs_assets()

    def import_mobs_assets(self):
        path = "graphics/Mobs/"
        for mob in self.assets.keys():
            new_path = f"{path}{mob}/"  
            for animation in self.assets[mob].keys():
                fullpath = f"{new_path}{animation}"
                self.assets[mob][animation] = import_folder(fullpath, mob)


mob_group = pygame.sprite.Group()
mob_hitbox_group = pygame.sprite.Group()
mob_assets = MobAnimation()
