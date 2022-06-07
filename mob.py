from distutils.spawn import spawn
import pygame
from settings import screen_width, floor
from random import randint, choice

mob_group = pygame.sprite.Group()

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        # Utility
        self.spawn_choice = choice([1, -1])
        self.spawn()
        
        # Attribute
        max_speed = 4
        min_speed = 2
        self.speed = randint(min_speed,max_speed)
        
    def spawn(self):
        height = 60
        width = 40
        self.image = pygame.Surface((width, height))
        self.image.fill("red")
        if self.spawn_choice == -1:
            self.rect = self.image.get_rect(midbottom=(screen_width-30, floor))
        else:
            self.rect = self.image.get_rect(midbottom=(30, floor))
        mob_group.add(self)


    def move(self):
        self.rect.x += self.speed * self.spawn_choice
        if self.rect.right <= 0 or self.rect.left >= screen_width:
            mob_group.remove(self)
        
    def update(self, screen):
        mob_group.draw(screen)
        self.move()
