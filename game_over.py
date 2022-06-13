import pygame

from settings import settings
from score import score
from mob import mob_hitbox_group, mob_group
from player import player

def check_player_collision():
    """Check if player collides with a mob.
    Reset the game"""
    if not player.is_invulnerable:
        mobs_hitten = pygame.sprite.groupcollide(mob_hitbox_group, player.hitbox, False, False)
        if len(mobs_hitten) != 0: 
            for mob in mobs_hitten.keys():
                if mob.status != "Death":
                    player.hp -= 1
                    if player.hp == 0:
                        settings.player_death.play().set_volume(0.5)
                        player.frame_index = 0
                        player.status = "Death"
                        player.animation_speed = 0.1
                        
                        mob_hitbox_group.empty()
                        mob_group.empty()
                        
                        settings.reset()
                        score.reset_score()
                        score.check_best_score()
                    else:
                        settings.player_hit.play()
                        player.go_invulnerable() 

def draw_intro_screen(screen):
    # Background
    intro_background_surf = pygame.Surface(settings.screen_size)
    pygame.Surface.fill(intro_background_surf, "#207a6b")
    intro_background_rect = intro_background_surf.get_rect(topleft = (0,0))
    screen.blit(intro_background_surf,intro_background_rect)
    # Avatar
    avatar_center = (600,150)
    avatar_surf = pygame.image.load("graphics/Knight/Idle/idle1.png").convert_alpha()
    avatar_surf = pygame.transform.scale2x(avatar_surf)
    avatar_rect = avatar_surf.get_rect(center=avatar_center)
    screen.blit(avatar_surf, avatar_rect)
    # Instructions / Score
    font_size = 40
    color = "#1d1f1f"
    font = pygame.font.Font("alagard.ttf", font_size)
    if settings.game_started:
        best_score_str = f"Best score:  {score.best_score}"
        score_str = f"Your score:  {score.user_score}"
        best_score_surf = pygame.font.Font.render(font, best_score_str, False, color)
        best_score_rect = best_score_surf.get_rect(topleft=(20, 60))
        screen.blit(best_score_surf, best_score_rect)
        score_surf = pygame.font.Font.render(font, score_str, False, color)
        score_rect = score_surf.get_rect(topleft=(20, 120))
        screen.blit(score_surf, score_rect)
    else:
        title_str = "You are ambushed!!!"
        title_surf = pygame.font.Font.render(font, title_str, False, color)
        title_rect = title_surf.get_rect(midtop=(settings.screen_width/2, 20))
        screen.blit(title_surf, title_rect)
        controls = ["Left / Right: Arrows", "Jump: up arrow", "Super Attack: left shift"]
        for index, control in enumerate(controls):
            surf = pygame.font.Font.render(font, control, False, color)
            y_pos = 120 + 60 * index 
            rect = surf.get_rect(topleft=(20, y_pos))
            screen.blit(surf, rect)
    start_str = "Hit Return to start"
    start_surf = pygame.font.Font.render(font, start_str, False, color)
    start_rect = start_surf.get_rect(midtop=(settings.screen_width/2, 320))
    screen.blit(start_surf, start_rect)
    