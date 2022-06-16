import pygame
import sys
from random import randint

from settings import settings
from support import cursor
from score import score
from sprite_group import groups
from player import player
from mob import Mob
import game_over

pygame.display.set_caption("Ambush")
clock = pygame.time.Clock()
settings.create_spawn_timer()

background_rect, background_surf = settings.create_background()
settings.play_background_music()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            score.save_best_score()
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                settings.game_active = True
                settings.game_started = True
        # Game started
        if settings.game_active:
            if event.type == settings.player_attacking_timer:
                pygame.time.set_timer(settings.player_attacking_timer, 0)
                player.is_attacking = False
            if event.type == settings.player_attack_delay_timer:
                pygame.time.set_timer(settings.player_attack_delay_timer, 0)
                player.can_attack = True
            if event.type == settings.player_invulnerability_timer:
                pygame.time.set_timer(settings.player_invulnerability_timer, 0)
                player.is_invulnerable = False
                groups["shield"].empty()
            if event.type == settings.spawn_timer:
                if player.status != "Death":
                    Mob()
                    pygame.time.set_timer(settings.spawn_timer, 
                                          randint(settings.difficulty, 
                                                  settings.difficulty + 500))

    if settings.game_active:
        # background
        settings.screen.blit(background_surf, background_rect)

        # player and mobs
        groups["mobs"].draw(settings.screen)
        groups["player"].update()
        groups["mobs"].update()

        # score
        score.display_scores()
        settings.scale_difficulty()

        # collisions
        game_over.check_player_collision()

    else:
        game_over.draw_intro_screen()

    pygame.display.update()
    clock.tick(60)
