import pygame

from settings import settings
from score import score
from support import import_folder
from super import SuperAttack
from mob import mob_group, mob_hitbox_group


class Player(pygame.sprite.Sprite):
    '''Sprite class of the player'''
    def __init__(self):
        super().__init__()
        self.import_character_assets()
        
        # Hit box
        self.hitbox_sprite = HitBox()
        self.hitbox = pygame.sprite.GroupSingle()
        self.hitbox.add(self.hitbox_sprite)
        
        # Character sprite
        self.frame_index = 0
        self.animation_speed = 0.3
        self.image = self.animations["Stand"][0]
        self.rect = self.image.get_rect(bottomleft=self.hitbox_sprite.rect.bottomleft)
        self.group = pygame.sprite.GroupSingle()
        self.group.add(self)
        
        # Hit sprite
        self.hit = HitSprite()

        # Attribute
        self.speed = 4
        self.jump_speed = -16
        
        # Attack
        self.attacking_timer = pygame.USEREVENT + 1
        self.attack_delay_timer = pygame.USEREVENT + 2
        self.attack_duration = 200
        self.attack_delay = 400
        self.can_attack = True
        self.is_attacking = False
        
        # Super attack
        self.super_attack_charge = 0
        self.super_max_charge = 100
        self.super_charge_speed = 0.2
        self.can_super_attack = False
        self.is_super_attacking = False
        self.super_atack_shockwave = False
        self.charge_rect = pygame.Rect(50,50,self.super_attack_charge, 15)
        self.charge_border_rect = pygame.Rect(50,50,200, 15)
        self.super_group = pygame.sprite.Group()

        # Utility
        self.gravity = 0.8
        self.direction = pygame.Vector2(0,0)
        self.is_moving = False
        self.is_going_right = True
        self.status = "Stand"
    
    def charge_super_attack(self):
        self.super_attack_charge += self.super_charge_speed
        
    def check_super_attack(self):
        if self.super_attack_charge >= self.super_max_charge:
            self.super_attack_charge = self.super_max_charge
            self.can_super_attack = True
            
    def super_shockwave(self):
        if self.super_atack_shockwave:
            super_attack = SuperAttack(self.is_going_right, self.rect.bottomleft, self.rect.bottomright)
            self.super_group.add(super_attack)
            self.super_atack_shockwave = False

    def stick_character_to_hitbox(self):
        """Stick the character rect to the hitbox rect according to the player's direction"""
        # self.image = self.animations["Run_Attack"][3]
        self.animate()
        if self.is_going_right:
            self.rect.midbottom = self.hitbox_sprite.rect.bottomright
        else:
            self.image = pygame.transform.flip(self.image, True, False)
            self.rect.midbottom = self.hitbox_sprite.rect.bottomleft
    
    def animate(self):
        '''Animate player'''
        ancient_status = self.status
        self.get_status()
        self.frame_index += self.animation_speed
        if len(self.animations[self.status]) == 0: self.frame_index = 0
        elif self.status != ancient_status: self.frame_index = 0
        elif self.frame_index >= len(self.animations[self.status]) or self.status != ancient_status:
            self.frame_index = 0
            if self.is_super_attacking:
                self.is_super_attacking = False
                self.super_atack_shockwave = True
        self.image = self.animations[self.status][int(self.frame_index)]
        
    def get_status(self):
        """Get the good status according to player's input."""
        # Attack
        if self.is_super_attacking:
            self.status = "Attack_Extra"
        elif self.is_attacking:
            self.status = "Attack"
        # jump
        elif self.hitbox_sprite.rect.bottom != settings.floor: 
            self.status = "Jump"
        # Run
        elif self.is_moving: 
            self.status = "Run"
        # stand
        else: self.status = "Stand"
        
    def import_character_assets(self):
        """Import character's assests"""
        character_path = "graphics/Knight/"
        self.animations = {
            "Attack": [],
            "Run": [],
            "Jump": [],
            "Attack_Extra": [],
            "Stand": [],
        }
        for animation in self.animations.keys():
            full_path  = character_path + animation
            self.animations[animation] = import_folder(full_path, "Knight")

    def apply_gravity(self):
        '''Applies gravity to the player'''
        self.direction.y += self.gravity
        self.hitbox_sprite.rect.y += self.direction.y
        if self.hitbox_sprite.rect.bottom >= settings.floor:
            self.hitbox_sprite.rect.bottom = settings.floor

    def user_inputs(self):
        '''Checks user's inputs and acts in consequence'''
        self.is_moving = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.is_going_right = False
            self.is_moving = True
            self.hitbox_sprite.rect.x -= self.speed
            if self.hitbox_sprite.rect.left < 0:
                self.hitbox_sprite.rect.left = 0
        if keys[pygame.K_RIGHT]:
            self.is_going_right = True
            self.is_moving = True
            self.hitbox_sprite.rect.x += self.speed
            if self.hitbox_sprite.rect.right > settings.screen_width:
                self.hitbox_sprite.rect.right = settings.screen_width
        if keys[pygame.K_UP] and self.hitbox_sprite.rect.bottom == settings.floor:
            self.direction.y = self.jump_speed
            self.is_moving = False
        if keys[pygame.K_SPACE]:
            if self.can_attack:
                self.is_attacking = True
                self.can_attack = False
                pygame.time.set_timer(self.attacking_timer, self.attack_duration)
                pygame.time.set_timer(self.attack_delay_timer, self.attack_delay)
        if keys[pygame.K_LSHIFT]:
            if self.can_super_attack and self.hitbox_sprite.rect.bottom == settings.floor:
                self.super_attack_charge = 0
                self.can_super_attack = False
                self.is_super_attacking = True
            
    def draw_super_attack_charge(self, screen):
        self.charge_rect.width = self.super_attack_charge * 2
        if self.super_attack_charge < 20:
            color = "red"
        elif self.super_attack_charge < 40:
            color = "orange"
        elif self.super_attack_charge < 60:
            color = "yellow"
        elif self.super_attack_charge < 80:
            color = "green"
        elif self.super_attack_charge < 100:
            color = "#05e7f7"
        else:
            color = "blue"
        
        pygame.draw.rect(screen, color, self.charge_rect)
        pygame.draw.rect(screen, "black", self.charge_border_rect, 2)
            
    def check_super_attack_collisions(self):
        hit_points = 100

        mobs_hitten = pygame.sprite.groupcollide(mob_hitbox_group, self.super_group,False, False)
        for mob_hitbox in mobs_hitten.keys():
            if not mob_hitbox.is_invincible: 
                mob_hitbox.frame_index = 0
                mob_hitbox.hp -= 1
                score.score += hit_points
                if mob_hitbox.hp == 0:
                    mob_hitbox.status = "Death"
                    mob_hitbox.speed = 0
            mob_hitbox.is_invincible = True
            mob_hitbox.start_point_x = mob_hitbox.rect.x
        
    def update(self, screen):
        self.group.draw(screen)
        self.hit.group.draw(screen)
        self.super_shockwave()
        self.super_group.draw(screen)
        
        self.user_inputs()
        self.apply_gravity()
        self.stick_character_to_hitbox()
        
        self.charge_super_attack()
        self.check_super_attack()
        self.draw_super_attack_charge(screen)

        self.hit.update(self)
        self.super_group.update()
              

class HitBox(pygame.sprite.Sprite):
    '''Hit box sprite class. Utilize it to align character's rect on it  and for collision'''
    def __init__(self):
        super().__init__()
        starting_point = (settings.screen_width/2, settings.floor)
        size = (40,60)
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(midbottom=starting_point)


class HitSprite(pygame.sprite.Sprite):
    '''A class that represents the hit box of the attack of the player'''
    def __init__(self):
        super().__init__()
        size = (35, 60)
        self.image = pygame.Surface(size)
        self.image.set_alpha(0)
        self.rect = self.image.get_rect(bottomright=(0,0))
        self.group = pygame.sprite.GroupSingle()
        self.group.add(self)

    def check_direction_and_status(self, player):
        '''Place hit box according to player direction and if player is attacking'''
        if player.is_attacking:
            if player.is_going_right:
                self.rect.bottomleft = player.hitbox_sprite.rect.bottomright
            else:
                self.rect.bottomright = player.hitbox_sprite.rect.bottomleft
        else:
            self.rect.bottomright = (0,0)

    def check_collision(self):
        '''Checks collisions between the hit zone and any ennemi'''
        hit_points = 100
        mobs_hitten = pygame.sprite.groupcollide(mob_hitbox_group, self.group,False, False)
        for mob_hitbox in mobs_hitten.keys():
            if not mob_hitbox.is_invincible: 
                mob_hitbox.frame_index = 0
                mob_hitbox.hp -= 1
                score.score += hit_points
                if mob_hitbox.hp == 0:
                    mob_hitbox.status = "Death"
                    mob_hitbox.speed = 0
            mob_hitbox.is_invincible = True
            mob_hitbox.start_point_x = mob_hitbox.rect.x
        

    def update(self, player):
        self.check_direction_and_status(player)
        self.check_collision()


player = Player()
