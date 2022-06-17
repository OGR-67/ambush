from random import choice
from math import floor
import pygame
import utility_classes
from settings import settings
from sprite_group import groups
from score import score


class Mob(utility_classes.AnimatedSprite):
    """The Mob class represents a mob. Mob type and position are randomly chosen
    at initialization. Mob have a hitbox created with the MobHitbox class."""
    def __init__(self):
        mob_types = ["demon", "lizard", "jinn", "lizard", "jinn"]
        animation_dict = {"Walk": [], "Death": [], "Hurt": []}
        self.type = str(choice(mob_types))
        self.spawn_choice = choice([1, -1])
        self.moving_right = True if self.spawn_choice == 1 else False
        self.direction_right = self.moving_right
        super().__init__(self.type, "graphics/Mobs", animation_dict)
        self.status = "Walk"
        # Spawn
        self.spawn()
        self.stick_asset_to_hibox()
        
        self.ancient_status = self.status
        self.is_invincible = False

    def spawn(self):
        """Set position and size of hitbox. Set speed of mob.
        Add mob to mobs group, hitbox to mobs_hitbox group'"""
        rect_bottom = settings.floor
        match self.type:
            case "demon":
                self.speed = 2
                size = settings.demon_size
            case "lizard": 
                self.speed = 4
                size = settings.lizard_size
            case "jinn": 
                self.speed = 3
                jinn_vertical_shift = -50
                size = settings.jinn_size
                rect_bottom += jinn_vertical_shift
        self.hitbox = MobHitbox(size)
        self.hp = 2 if self.type == "demon" else 1
        if self.spawn_choice == -1:
            self.hitbox.rect.midbottom = (settings.screen_width - 30, rect_bottom)
        else: self.hitbox.rect.midbottom = (30, rect_bottom)
        groups["mobs"].add(self)
        groups["mobs_hitbox"].add(self.hitbox)

    def check_status_change(self):
        """Check any changement of status.
        Set frame_index to 0 if any"""
        if self.status != self.ancient_status:
            self.frame_index = 0

    def stick_asset_to_hibox(self):
        """Stick asset to the hitbox"""
        match self.type:
            case "demon":
                shift_y = 15
                shift_x = 30 * self.spawn_choice
            case "jinn":
                shift_y = 15
                shift_x = 10 * self.spawn_choice
            case "lizard":
                shift_y = 0
                shift_x = 0 * self.spawn_choice
        self.rect.centerx = self.hitbox.rect.centerx + shift_x
        self.rect.centery = self.hitbox.rect.top + shift_y

    def move(self):
        """Move hitbox."""
        if self.is_invincible: self.hurt()
        else: self.hitbox.rect.x += self.speed * self.spawn_choice

    def hurt(self):
        """Hurt movement logic"""
        offset_x = 30 * self.spawn_choice
        self.status = "Hurt"
        self.hitbox.rect.x -= self.speed * self.spawn_choice
        if self.hitbox.rect.x == self.hitbox.start_point_x - offset_x:
            self.is_invincible = False
            self.status = "Walk"

    def kill_out_of_screen(self):
        """Kill sprite and its hitbox when out of screen."""
        if self.hitbox.rect.right <= -50 or \
        self.hitbox.rect.left >= settings.screen_width + 50:
            self.kill()
            self.hitbox.kill()

    def mobs_collisions(self, group):
        """Check collision between mobs and specified group."""
        mob_collided_hitbox = pygame.sprite.groupcollide(groups["mobs_hitbox"], group,False, False)
        if mob_collided_hitbox is not {}:
            for mob_hitbox in mob_collided_hitbox.keys():
                if self.hitbox == mob_hitbox:
                    if not self.is_invincible:
                        self.frame_index = 0
                        self.hp -= 1
                        score.score += settings.points_on_death
                        choice(settings.mob_sounds["hit"]).play()

                        if self.hp == 0:
                            self.frame_index = 0
                            self.speed = 0
                            def new_hurt(): pass
                            self.hurt = new_hurt
                            self.animate = self.death_animate
                            choice(settings.mob_sounds["death"]).play()
                    self.is_invincible = True
                    self.hitbox.start_point_x = mob_hitbox.rect.x

    def death_animate(self):
        """
        Animation for dying mob. When animation ends:
        - kill hitbox
        - kill sprite
        """
        image_to_animate = self.frames["Death"]
        self.frame_index += self.animation_speed
        index = floor(self.frame_index) 
        if index >= len(image_to_animate):
            index = self.frame_index = 0
            self.hitbox.kill()
            self.kill()
        self.image = image_to_animate[index]

    def clear_if_dead(self):
        """Delete hitbox and sprite when in no group."""
        if not self.groups():
            del self.hitbox
            del self

    def update(self):
        screen = settings.screen
        self.check_status_change()
        self.move()
        self.animate()
        self.stick_asset_to_hibox()
        self.kill_out_of_screen()
        self.mobs_collisions(groups["super"])
        self.mobs_collisions(groups["hit"])
        self.clear_if_dead()


class MobHitbox(utility_classes.HitboxSprite):
    """Mob hitbox is a simple sprite of a simple rect used for 
    collision and placement"""
    def __init__(self, size):
        super().__init__(size)
        self.start_point_x = 0
