from utility_classes import AnimatedSprite


class Shield(AnimatedSprite):
    """Shield class is a simple animated class that represents
    a shield. This is used for feedback of invulnerability frames"""
    def __init__(self, player):
        """Takes player argument for placement on the player sprite."""
        super().__init__("Shield", "graphics/", None)
        self.player = player
        self.frame_index = 0
        self.rect = self.image.get_rect(center=self.player.rect.center)
        self.animation_speed = 1

    def stick_to_char(self):
        """Stick sprite on player spite"""
        self.rect = self.image.get_rect(center=self.player.rect.center)

    def update(self):
        self.animate()
        self.stick_to_char()
