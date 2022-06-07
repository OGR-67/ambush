from distutils.spawn import spawn
import pygame
import sys
from player import Player
from mob import Mob, mob_group
from settings import *
from game_over import check_player_collision
from random import randint

pygame.init()

screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Melee Warrior")
clock = pygame.time.Clock()
background_image = pygame.image.load("graphics/Battleground3.png").convert()
background_surf = pygame.transform.scale(background_image, (screen_width, screen_height))
background_rect = background_surf.get_rect(topleft=(0,0))

player = Player()

spawn_timer = pygame.USEREVENT + 3
pygame.time.set_timer(spawn_timer, randint(1000, 1500))
 
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == player.attacking_timer:
            pygame.time.set_timer(player.attacking_timer, 0)
            player.is_attacking = False
        if event.type == player.attack_delay_timer:
            pygame.time.set_timer(player.attack_delay_timer, 0)
            player.can_attack = True
        if event.type == spawn_timer:
             Mob()
             pygame.time.set_timer(spawn_timer, randint(1000, 1500))
    
    screen.blit(background_surf, background_rect)
    
    # Draw here
    player.update(screen, mob_group)
    mob_group.update(screen)
        
    # Update here
    check_player_collision(player, mob_group)
    
    pygame.display.update()
    clock.tick(60)
