import pygame
import sys
from random import randint
from settings import settings
from support import cursor
screen = pygame.display.set_mode(settings.screen_size) # Needs to be set here before creating sprites
from score import score
from player import player
from mob import Mob, mob_group
from game_over import check_player_collision, draw_intro_screen


def create_background():
    background_image = pygame.image.load("graphics/Battleground.png").convert()
    background_surf = pygame.transform.scale(background_image, (settings.screen_width, settings.screen_height))
    background_rect = background_surf.get_rect(topleft=(0,0))
    return background_rect, background_surf

def play_music():
    pygame.mixer.music.load("sounds/background_music.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

pygame.display.set_caption("Melee Warrior")
clock = pygame.time.Clock()

background_rect, background_surf = create_background()
play_music()

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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                settings.game_active = True
                settings.game_started = True
        # Game started
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
                if player.status != "Death":
                    Mob()
                    pygame.time.set_timer(spawn_timer, randint(settings.difficulty, settings.difficulty+500))

    if settings.game_active:
        # background
        screen.blit(background_surf, background_rect)
        # player and mobs
        player.update(screen)
        mob_group.update(screen)
        # score
        score.blit_score(screen)
        settings.scale_difficulty()
        score.set_score(settings.difficulty, settings.max_difficulty)
        # collisions
        check_player_collision()
        player.check_super_attack_collisions()
        # Cursor
        # for item in player.heart_group.sprites():
        #     cursor(screen, "red", item.rect)
    
    else: draw_intro_screen(screen)
    
    pygame.display.update()
    clock.tick(60)
