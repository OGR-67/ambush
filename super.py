import pygame
from utility_classes import AnimatedSprite


class ChargedChar(AnimatedSprite):
    """ChargedChar class represents turning orb that is used as feedback
    for super attack full charge."""
    def __init__(self, player):
        """Takes a player for argument. This is used to place sprite on
        the character."""
        super().__init__("Charged", "graphics/", None)
        self.player = player
        self.rect = self.image.get_rect(center=self.player.rect.center)
        self.animation_speed = 0.20 

    def stick_to_char(self):
        """Stick sprite on the player."""
        self.rect = self.image.get_rect(center=self.player.rect.center)

    def update(self):
        self.animate()
        self.stick_to_char()


class ChargedBar(AnimatedSprite):
    """Represents electric effects for full super attack charged
    bar."""
    def __init__(self, charge_bar):
        """Takes charge_bar parameters for placement"""
        super().__init__("Charged_bar", "graphics/", None)
        self.rect = self.image.get_rect(center=charge_bar.center)
        self.animation_speed = 0.6

    def update(self):
        self.animate()


class SuperAttack(AnimatedSprite):
    """SuperAttack class is for super attack shockwave."""
    def __init__(self, is_going_right, player_bottomleft, player_bottomright):
        """
        - is_going_right: is the player going right?
        - player_bottomleft: player's sprite bottom left coordinate
        - player_bottomright: player's sprite bottom right coordinate
        """
        super().__init__("Super", "graphics/", None)
        self.animation_speed = 0.4
        self.is_going_right = is_going_right
        self.get_rect(player_bottomleft, player_bottomright)
        self.is_over = False
        self.speed = 4

    def get_rect(self, player_bottomleft, player_bottomright):
        """Get initial rect from player_bottomleft and player_bottomright
        because position depends on player's direction."""
        shift_x = 120
        shift_y = 120
        if self.is_going_right:
            self.rect = self.image.get_rect(bottomleft=player_bottomright)
            self.rect.x -= shift_x
        else:
            self.rect = self.image.get_rect(bottomright=player_bottomleft)
            self.rect.x += shift_x
        self.rect.y += shift_y

    def move(self):
        """Move shockwave to the opposite side of the player."""
        if self.is_going_right:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

    def flip(self):
        """Flips the image horizontally if shockwave is going left."""
        if not self.is_going_right:
            self.image = pygame.transform.flip(self.image, True, False)

    def kill_if_done(self):
        """Kills the sprite when shockwave's animation finishes."""
        if self.frame_index > len(self.frames) and self.has_started: 
            self.frame_index = 0
            self.is_over = True
            self.kill()

    def update(self):
        if not self.is_over:
            self.move()
            self.animate()
            self.flip()
            self.kill_if_done()
