import pygame

groups = {
    "player": pygame.sprite.GroupSingle(),
    "player_hitbox": pygame.sprite.GroupSingle(),
    "mobs": pygame.sprite.Group(),
    "mobs_hitbox": pygame.sprite.Group(),
    "hit": pygame.sprite.GroupSingle(),
    "heart": pygame.sprite.Group(),
    "super": pygame.sprite.Group(),
    "charged": pygame.sprite.Group(),
    "shield": pygame.sprite.GroupSingle(),
    }