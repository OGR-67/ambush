import pygame

from settings import settings
from score import score
from player import player
from sprite_group import groups
from blood import blood 


def check_player_collision():
    """Check if player collides with a mob."""
    if not player.is_invulnerable:
        mobs_hitbox_hitten = pygame.sprite.groupcollide(
            groups["mobs_hitbox"], 
            groups["player_hitbox"], 
            False, False)
        for mob_hitbox in mobs_hitbox_hitten.keys():
            for mob in groups["mobs"].sprites():
                if mob.hitbox == mob_hitbox:
                    if not mob.is_invincible:
                        player.hp -= 1
                        if player.hp == 0:
                            player_dead()
                        else:
                            settings.player_hit.play()
                            player.go_invulnerable()

def player_dead():
    """
    Empty mob_hitbox, mobs and heart groups, reset settings and for the player:
    - Play death sound
    - Set status to Death
    - Set is_dying to True.
    - Slow down animation speed
    """
    settings.player_death.play().set_volume(0.5)
    player.frame_index = 0
    player.status = "Death"
    player.is_dying = True
    player.animation_speed = 0.1
    groups["mobs_hitbox"].empty()
    groups["mobs"].empty()
    groups["heart"].remove(blood)
    settings.reset()

def set_and_draw_intro_background():
    """Set and draw the background of the intro screen."""
    intro_background_surf = pygame.Surface(settings.screen_size)
    pygame.Surface.fill(intro_background_surf, "#207a6b")
    intro_background_rect = intro_background_surf.get_rect(topleft = (0,0))
    settings.screen.blit(intro_background_surf,intro_background_rect)

def set_and_draw_intro_avatar():
    """Set and draw the avatar of the intro screen."""
    avatar_center = (600,150)
    avatar_surf = pygame.image.load(
        "graphics/Knight/Idle/idle1.png").convert_alpha()
    avatar_surf = pygame.transform.scale2x(avatar_surf)
    avatar_rect = avatar_surf.get_rect(center=avatar_center)
    settings.screen.blit(avatar_surf, avatar_rect)

def set_and_draw_intro_scrore():
    """Set and draw current score on the intro screen."""
    score_str = f"Your score:  {score.user_score}"
    score_surf = pygame.font.Font.render(
        settings.intro_font,
        score_str,
        False,
        settings.intro_color
        )
    score_rect = score_surf.get_rect(topleft=(20, 120))
    settings.screen.blit(score_surf, score_rect)

def set_and_draw_intro_best_scrore():
    """Set and draw best score on the intro screen."""
    best_score_str = f"Best score:  {score.best_score}"   
    best_score_surf = pygame.font.Font.render(
        settings.intro_font,
        best_score_str,
        False,
        settings.intro_color
        )
    best_score_rect = best_score_surf.get_rect(topleft=(20, 60))
    settings.screen.blit(best_score_surf, best_score_rect)

def set_and_draw_intro_title():
    """Set and draw intro screen's title."""
    title_str = "You are ambushed!!!"
    title_surf = pygame.font.Font.render(
        settings.intro_font,
        title_str,
        False,
        settings.intro_color
        )
    title_rect = title_surf.get_rect(midtop=(settings.screen_width/2, 20))
    settings.screen.blit(title_surf, title_rect)

def set_and_draw_intro_controls():
    """Set and draw the controls on the intro screen."""
    controls = ["Left / Right: Arrows", "Jump: up arrow", "Super Attack: left shift"]
    for index, control in enumerate(controls):
        surf = pygame.font.Font.render(
            settings.intro_font,
            control,
            False,
            settings.intro_color
            )
        y_pos = 120 + 60 * index 
        rect = surf.get_rect(topleft=(20, y_pos))
        settings.screen.blit(surf, rect)

def set_and_draw_intro_start():
    start_str = "Hit Return to start"
    start_surf = pygame.font.Font.render(
        settings.intro_font, 
        start_str,
        False,
        settings.intro_color
        )
    start_rect = start_surf.get_rect(midtop=(settings.screen_width/2, 320))
    settings.screen.blit(start_surf, start_rect)

def draw_intro_screen():
    """Draw the intro screen."""
    set_and_draw_intro_background()
    set_and_draw_intro_avatar()
    if settings.game_started:
        set_and_draw_intro_scrore()
        set_and_draw_intro_best_scrore()
    else:
        set_and_draw_intro_title()
        set_and_draw_intro_controls()
    set_and_draw_intro_start()
