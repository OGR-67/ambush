from random import choice
import pygame

from sprite_group import groups
from settings import settings
from utility_classes import AnimatedSprite, HitboxSprite
import super as sp
from shield import Shield
from heart import heart
from blood import blood
from score import score

class Player(AnimatedSprite):
    """Sprite class of the player"""
    def __init__(self):
        knight_animations_dict = {
            "Attack": [],
            "Run": [],
            "Jump": [],
            "Attack_Extra": [],
            "Stand": [],
            "Death": [],
        }
        self.direction_right = True
        super().__init__("Knight", "graphics", knight_animations_dict)
        self.animation_speed = 0.3

        # Player
        self.hitbox = HitboxSprite(settings.player_hitbox_size)
        self.hitbox.rect.midbottom = settings.player_starting_point_coods
        groups["player_hitbox"].add(self.hitbox)
        groups["player"].add(self)

        # Hit sprite
        self.hit = HitSprite()

        # Attribute
        self.speed = 4
        self.jump_speed = -16
        self.hp = 3

        # Attack
        self.can_attack = True
        self.is_attacking = False

        # Super attack
        self.super_attack_charge = 0
        self.can_super_attack = False
        self.is_super_attacking = False
        self.super_atack_shockwave = False
        self.charge_rect = pygame.Rect(
            settings.Charge_bar_coordinates_x,
            settings.Charge_bar_coordinates_y,
            self.super_attack_charge,
            settings.Charge_bar_height
            )
        self.charge_border_rect = pygame.Rect(
            settings.Charge_bar_coordinates_x,
            settings.Charge_bar_coordinates_y,
            settings.Charge_bar_max_width,
            settings.Charge_bar_height
            )
        self.charged_char = sp.ChargedChar(self.hitbox)
        self.charged_bar = sp.ChargedBar(self.charge_border_rect)

        # invulnerablity frame
        self.is_invulnerable = False
        self.is_dying = False
        self.shield = Shield(self.hitbox)

        # Utility
        self.gravity = 0.8
        self.direction = pygame.Vector2(0,0)
        self.is_moving = False
        self.is_going_right = True
        self.status = "Stand"

    def set_heart_frame_index(self):
        """Set heart frame index based on player's hp."""
        heart.frame_index = 3 - self.hp
        if heart.frame_index == 2:
            groups["heart"].add(blood)
        if heart.frame_index >= len(heart.frames):
            groups["heart"].remove(blood)
            heart.frame_index = 3
        heart.image = heart.frames[heart.frame_index]

    def charge_super_attack(self):
        """Increment value of super attack charge"""
        self.super_attack_charge += settings.super_charge_speed

    def check_super_attack(self):
        """If super attack is full charged, add charged_char and charged_bar to
        'charged' group and set can_super_attack to True"""
        if self.super_attack_charge >= settings.super_max_charge:
            self.super_attack_charge = settings.super_max_charge
            self.can_super_attack = True
            groups["charged"].add([self.charged_char, self.charged_bar])

    def get_charge_bar_color(self):
        """
        Return the color of the charge bar based on super_attack_charge value.
        """
        if self.super_attack_charge < 20: return "#fc3a3a"
        if self.super_attack_charge < 40: return "#eb7107"
        if self.super_attack_charge < 60: return "#cde630"
        if self.super_attack_charge < 80: return "#56f03e"
        if self.super_attack_charge < 100: return "#42ecf5"
        return "#e6e6fc"

    def draw_super_attack_charge(self):
        """Draw charge bar of super attack."""
        self.charge_rect.width = self.super_attack_charge * 2
        color = self.get_charge_bar_color()
        pygame.draw.rect(settings.screen, color, self.charge_rect)

    def draw_super_attack_charge_border(self):
        """Draw the border of the super attack charge bar."""
        border_size = 2
        border_color = "black"
        pygame.draw.rect(
            settings.screen,
            border_color,
            self.charge_border_rect,
            border_size
            )

    def super_shockwave(self):
        """Create shockwave sprite, spawn it to the good side of the player
        and add it to the group"""
        if self.super_atack_shockwave:
            settings.shockwave.play()
            super_attack = sp.SuperAttack(
                self.is_going_right,
                self.rect.bottomleft,
                self.rect.bottomright
                )
            groups["super"].add(super_attack)
            self.super_atack_shockwave = False

    def stick_character_to_hitbox(self):
        """
        Stick the character rect to the hitbox rect according
        to the player's direction
        """
        self.animate_player()
        if self.status == "Death":
            self.rect.bottomright = self.hitbox.rect.center
        else:
            if self.is_going_right:
                self.rect.midbottom = self.hitbox.rect.bottomright
            else:
                self.image = pygame.transform.flip(self.image, True, False)
                self.rect.midbottom = self.hitbox.rect.bottomleft

    def animate_player(self):
        '''Animate player'''
        ancient_status = self.status
        self.get_status()
        self.frame_index += self.animation_speed
        # Single frame
        if len(self.frames[self.status]) == 0: self.frame_index = 0
        # New status -> index to 0
        elif self.status != ancient_status:
            self.frame_index = 0
        # End and reset game when death animation ends
        elif self.status == "Death" and \
        self.frame_index >= len(self.frames[self.status]):
            self.status = "Stand"
            settings.game_active =  False
            score.reset_score()
            score.check_best_score()
            self.reset()
        # Basic animation
        elif self.frame_index > len(self.frames[self.status]) or \
        self.status != ancient_status:
            self.frame_index = 0
            # Super attack case
            if self.is_super_attacking:
                self.is_super_attacking = False
                self.super_atack_shockwave = True
        # set image
        self.image = self.frames[self.status][int(self.frame_index)]

    def get_status(self):
        """Get the good status according to character situation."""
        if self.status == "Death": pass
        elif self.is_super_attacking:
            self.status = "Attack_Extra"
        elif self.is_attacking:
            self.status = "Attack"
        elif self.hitbox.rect.bottom != settings.floor:
            self.status = "Jump"
        elif self.is_moving:
            self.status = "Run"
        else: self.status = "Stand"

    def apply_gravity(self):
        '''Applies gravity to the player'''
        self.direction.y += self.gravity
        self.hitbox.rect.y += self.direction.y
        self.hitbox.rect.y = min(self.hitbox.rect.y, settings.floor)
        self.hitbox.rect.bottom = min(self.hitbox.rect.bottom, settings.floor)

    def player_left(self):
        """Get the character moving left."""
        self.is_going_right = False
        self.is_moving = True
        self.hitbox.rect.x -= self.speed
        self.hitbox.rect.x = max(self.hitbox.rect.x, 0)

    def player_right(self):
        """Get the character moving right."""
        self.is_going_right = True
        self.is_moving = True
        self.hitbox.rect.x += self.speed
        self.hitbox.rect.x = min(self.hitbox.rect.x, settings.screen_width)

    def jump(self):
        """Get the character jumping."""
        choice(settings.player_sounds["jump"]).play()
        self.direction.y = self.jump_speed
        self.is_moving = False

    def attack(self):
        """Get the character attacking."""
        sound = choice(settings.player_sounds["attack"])
        sound.set_volume(0.5)
        sound.play()
        self.is_attacking = True
        self.can_attack = False
        pygame.time.set_timer(
            settings.player_attacking_timer,
            settings.attack_duration,
            )
        pygame.time.set_timer(
            settings.player_attack_delay_timer,
            settings.attack_delay
            )

    def super_attack(self):
        """Get the character super attacking."""
        choice(settings.player_sounds["heavyattack"]).play()
        groups["charged"].empty()
        self.super_attack_charge = 0
        self.can_super_attack = False
        self.is_super_attacking = True
        self.go_invulnerable()

    def user_inputs(self):
        '''Checks user's inputs and acts in consequence'''
        self.is_moving = False
        if self.status != "Death":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]: self.player_left()
            if keys[pygame.K_RIGHT]: self.player_right()
            if keys[pygame.K_UP] and self.hitbox.rect.bottom == settings.floor:
                self.jump()
            if keys[pygame.K_SPACE]:
                if self.can_attack: self.attack()
            if keys[pygame.K_LSHIFT]:
                if self.can_super_attack and \
                    self.hitbox.rect.bottom == settings.floor:
                    self.super_attack()

    def reset(self):
        """Reset player when game's over"""
        self.is_dying = False
        self.hp = 3
        self.super_attack_charge = 0
        self.can_super_attack = False
        groups["super"].empty()
        groups["charged"].empty()
        groups["heart"].remove(blood)
        self.frame_index = 0
        self.animation_speed = 0.3
        self.status = "Stand"
        self.hitbox.rect.midbottom = (
            settings.screen_width / 2,
            settings.floor
            )

    def go_invulnerable(self):
        """Go invulnerable for some frames whith a shield as feedback"""
        settings.shield.play()
        groups["shield"].add(self.shield)
        self.is_invulnerable = True
        pygame.time.set_timer(
            settings.player_invulnerability_timer,
            settings.invulnerability_duration
            )

    def update(self):
        screen = settings.screen
        self.user_inputs()
        self.apply_gravity()
        self.stick_character_to_hitbox()
        self.charge_super_attack()
        self.check_super_attack()
        self.set_heart_frame_index()
        self.hit.update(self)
        self.draw_super_attack_charge()
        self.draw_super_attack_charge_border()
        self.super_shockwave()
        groups["super"].update()
        groups["shield"].update()
        groups["charged"].update()
        groups["heart"].update()
        groups["player"].draw(screen)
        groups["shield"].draw(screen)
        groups["super"].draw(screen)
        if self.status != "Death": groups["charged"].draw(screen)
        groups["heart"].draw(screen)


class HitSprite(HitboxSprite):
    '''A class that represents the hit box of the attack of the player'''
    def __init__(self):
        super().__init__(settings.player_hit_hitbox_size)
        groups["hit"].add(self)

    def check_direction_and_status(self, player):
        '''Place hit box according to player direction and
        attacking status.'''
        if player.is_attacking:
            if player.is_going_right:
                self.rect.bottomleft = player.hitbox.rect.bottomright
            else:
                self.rect.bottomright = player.hitbox.rect.bottomleft
        else:
            self.rect.bottomright = (0,0)

    def update(self, player):
        self.check_direction_and_status(player)


player = Player()
