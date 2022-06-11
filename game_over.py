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
        for mob in mobs_hitten.keys():
            if mob.status != "Death":
                # mob
                mob_hitbox_group.empty()
                mob_group.empty()
                
                # player
                player.super_attack_charge = 0
                player.can_super_attack = False
                player.super_group.empty()
                player.frame_index = 0
                player.status = "Stand"
                player.hitbox.sprite.rect.midbottom = (settings.screen_width/2, settings.floor)
                
                # score
                score.user_score = score.score
                score.score = 0
                settings.difficulty = settings.start_difficulty
                settings.game_active =  False
                if score.user_score > score.best_score:
                    score.best_score = score.user_score

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
    font = pygame.font.Font("alagard.ttf", font_size)
    if settings.game_started:
        instructions = f"Your score:  {score.user_score}"
    else:
        instructions = "Hit Return to start"
    instructions_center_pos = (300, settings.screen_height/2)
    instructions_surf = pygame.font.Font.render(font, instructions, False, "black")
    instructions_rect = instructions_surf.get_rect(center=instructions_center_pos)
    screen.blit(instructions_surf, instructions_rect)
    