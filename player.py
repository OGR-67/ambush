from email.mime import image
import pygame
from settings import floor, screen_width
from support import import_folder

class Player(pygame.sprite.Sprite):
    '''Sprite class of the player'''
    def __init__(self):
        super().__init__()
        self.import_character_assets()
        
        # Character sprite
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations["Run"][0]
        self.rect = self.image.get_rect(midbottom=(screen_width/2, floor))
        
            # --- trying stuff
        self.image.scroll(-15, -45) # !!! artefacts, why?
        self.rect.width = 60
        self.rect.height = 70
        
        self.group = pygame.sprite.GroupSingle()
        self.group.add(self)

        # Hit sprite
        self.hit = HitSprite(self)

        # Attribute
        self.speed = 4
        self.jump_speed = -14
        self.attack_duration = 150
        self.attack_delay = 500

        # Utility
        self.gravity = 0.8
        self.direction = pygame.Vector2(0,0)
        self.is_going_right = True
        self.is_attacking = False
        self.can_attack = True
        self.attacking_timer = pygame.USEREVENT + 1
        self.attack_delay_timer = pygame.USEREVENT + 2
        self.status = "Idle"
        
    def import_character_assets(self):
        character_path = "graphics/Knight/"
        self.animations = {
            "Attack": [],
            "Run": [],
            "Run_Attack": [],
            "Idle": [],
        }
        for animation in self.animations.keys():
            full_path  = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def apply_gravity(self):
        '''Applies gravity to the player'''
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
        if self.rect.bottom >= floor:
            self.rect.bottom = floor

    def user_inputs(self):
        '''Checks user's inputs and acts in consequence'''
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.is_going_right = False
            self.rect.x -= self.speed
            if self.rect.left < 0:
                self.rect.left = 0
        if keys[pygame.K_RIGHT]:
            self.is_going_right = True
            self.rect.x += self.speed
            if self.rect.right > screen_width:
                self.rect.right = screen_width
        if keys[pygame.K_UP] and self.rect.bottom == floor:
            self.direction.y = self.jump_speed
        if keys[pygame.K_SPACE]:
            if self.can_attack:
                self.is_attacking = True
                self.can_attack = False
                pygame.time.set_timer(self.attacking_timer, self.attack_duration)
                pygame.time.set_timer(self.attack_delay_timer, self.attack_delay)
        if keys[pygame.K_LSHIFT]:
            self.is_attacking = False

    def update(self, screen, mob):
        self.group.draw(screen)
        self.hit.group.draw(screen)
        self.user_inputs()
        self.apply_gravity()
        self.hit.update(self, mob)


class HitSprite(pygame.sprite.Sprite):
    '''A class that represents the hit box of the attack of the player'''
    def __init__(self, player):
        super().__init__()
        # Hit sprite
        self.image = pygame.Surface((20,60))
        self.image.fill("white")
        self.rect = self.image.get_rect(bottomright=(0,0))
        self.group = pygame.sprite.GroupSingle()
        self.group.add(self)

    def check_direction_and_status(self, player):
        '''Place hit box according to player direction and if player is attacking'''
        if player.is_attacking:
            if player.is_going_right:
                self.rect.bottomleft = player.rect.bottomright
            else:
                self.rect.bottomright = player.rect.bottomleft
        else:
            self.rect.bottomright = (0,0)

    def check_collision(self, mob_group):
        pygame.sprite.groupcollide(self.group, mob_group, False, True)

    def update(self, player, mob_group):
        self.check_direction_and_status(player)
        self.check_collision(mob_group)
