import pygame
import sys
from random import randint
from settings import settings
from support import cursor

screen = pygame.display.set_mode(settings.screen_size)

from score import score
from player import player
from mob import Mob, mob_group
from game_over import check_player_collision, draw_intro_screen


pygame.display.set_caption("Melee Warrior")
clock = pygame.time.Clock()
background_image = pygame.image.load("graphics/Battleground3.png").convert()
background_surf = pygame.transform.scale(background_image, (settings.screen_width, settings.screen_height))
background_rect = background_surf.get_rect(topleft=(0,0))

spawn_timer = pygame.USEREVENT + 3
pygame.time.set_timer(spawn_timer, randint(1000, 1500))
 
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            with open("best_score.txt", "w") as f:
                best_score_str = str(score.best_score)
                f.write(best_score_str)
                
            pygame.quit()
            sys.exit()
        if settings.game_active:
            if event.type == player.attacking_timer:
                pygame.time.set_timer(player.attacking_timer, 0)
                player.is_attacking = False
            if event.type == player.attack_delay_timer:
                pygame.time.set_timer(player.attack_delay_timer, 0)
                player.can_attack = True
            if event.type == player.invulnerability_timer:
                pygame.time.set_timer(player.invulnerability_timer, 0)
                player.is_invulnerable = False
                player.shield.empty()
            if event.type == spawn_timer:
                Mob()
                pygame.time.set_timer(spawn_timer, randint(settings.difficulty, settings.difficulty+500))
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    settings.game_active = True
                    settings.game_started = True

    if settings.game_active:
        screen.blit(background_surf, background_rect)
        
        # Draw here
        player.update(screen)
        mob_group.update(screen)
        
        # Cursor
        # for mob in mob_group.sprites():
        #     cursor(screen, "red", mob.hitbox_sprite.rect)
        
        # Update here
        score.blit_score(screen)
        check_player_collision()
        player.check_super_attack_collisions()
        settings.set_difficulty()
        score.set_score(settings.difficulty, settings.max_difficulty)
    else:
        draw_intro_screen(screen)
    
    pygame.display.update()
    clock.tick(60)
