import pygame

def check_player_collision(player, mob_group):
    if pygame.sprite.groupcollide(player.group, mob_group, False, False):
        pygame.quit()
