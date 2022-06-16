import pygame
from random import randint
from os import walk


class Settings:
    def __init__(self):
        pygame.init()
        # screen
        self.screen_width = 800
        self.screen_height = 400
        self.screen_size = self.get_screen_size()
        self.screen = pygame.display.set_mode(self.get_screen_size())
        # font
        self.font = pygame.font.Font("alagard.ttf", 25)
        self.intro_font = pygame.font.Font("alagard.ttf", 40)
        self.intro_color = "#1d1f1f"
        # floor
        self.floor = 300
        # game state
        self.game_active = False
        self.game_started = False
        # Player
        self.player_hitbox_size = (40,60)
        self.player_hit_hitbox_size = (35,60)
        self.player_starting_point_coods = self.get_starting_point()
        self.attack_duration = 200
        self.attack_delay = 400
        self.super_max_charge = 100
        self.super_charge_speed = 0.2
        self.Charge_bar_coordinates_x = 70
        self.Charge_bar_coordinates_y = 30
        self.Charge_bar_height = 15
        self.Charge_bar_max_width = 200
        self.invulnerability_duration = 1000
        # Mob
        self.demon_size = (60, 85)
        self.lizard_size = (70, 45)
        self.jinn_size = (40, 70)
        self.points_on_death = 100
        # difficulty
        self.max_difficulty = 200
        self.start_difficulty =  2000
        self.difficulty = self.get_start_difficulty()
        # score
        self.score = 0
        self.user_score = 0
        self.score_position_coordinates = (550, 50)
        # Sounds
        self.player_sounds = self.import_warrior_sound_effects()
        self.player_attack = pygame.mixer.Sound("sounds/audio_effects/Knight/attack.wav")
        self.player_death = pygame.mixer.Sound("sounds/audio_effects/Knight/death.wav")
        self.player_heavy_attack = pygame.mixer.Sound("sounds/audio_effects/Knight/heavyattack.wav")
        self.player_hit = pygame.mixer.Sound("sounds/audio_effects/Knight/hit.wav")
        self.player_jump = pygame.mixer.Sound("sounds/audio_effects/Knight/jump.wav")
        self.shockwave = pygame.mixer.Sound("sounds/audio_effects/shockwave.wav")
        self.shield = pygame.mixer.Sound("sounds/audio_effects/shield.wav")
        self.mob_hit = pygame.mixer.Sound("sounds/audio_effects/Mob/hit.wav")
        self.mob_death = pygame.mixer.Sound("sounds/audio_effects/Mob/death.wav")
        # Timers
        self.player_attacking_timer = pygame.USEREVENT + 1
        self.player_attack_delay_timer = pygame.USEREVENT + 2
        self.spawn_timer = pygame.USEREVENT + 3
        self.player_invulnerability_timer = pygame.USEREVENT + 4

    def get_screen_size(self):
        """Return a tuple of screen_width and screen_height."""
        return (self.screen_width, self.screen_height)

    def get_starting_point(self):
        """Return starting point midbottom coordinates."""
        return ((self.screen_width/2, self.floor))

    def get_start_difficulty(self):
        """return start_difficulty value."""
        return self.start_difficulty

    def reset(self):
        """Reset difficulty to start difficulty value."""
        self.difficulty = self.start_difficulty

    def scale_difficulty(self):
        """Scale difficulty until max_difficulty is reached."""
        if self.difficulty > self.max_difficulty:
            self.difficulty -= 1

    def create_background(self):
        """Return a tuple of background_rect and background_surf."""
        background_image = pygame.image.load("graphics/Battleground.png").convert()
        background_surf = pygame.transform.scale(background_image, (self.screen_width, self.screen_height))
        background_rect = background_surf.get_rect(topleft=(0,0))
        return background_rect, background_surf

    def play_background_music(self):
        """Load and play background music."""
        pygame.mixer.music.load("sounds/background_music.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

    def create_spawn_timer(self):
        """Set mobs spawn timer."""
        pygame.time.set_timer(self.spawn_timer, randint(1000, 1500))

    def import_warrior_sound_effects(self):
        """Import sounds effects."""
        effects = {"attack": [], "heavyattack": [], "hit": [], "jump": [], "death": []}
        path = "sounds/characters_soud_effects/Knight/"
        for effect in effects.keys():
            sound_object_list = []
            fullpath = path + effect
            for _, __, files in walk(fullpath):
                for file in files:
                    sound_object = pygame.mixer.Sound(f"{fullpath}/{file}")
                    sound_object_list.append(sound_object)
                effects[effect] = sound_object_list
        return effects

    def import_mobs_sound_effects(self):
        """Import sounds effects."""
        pass

settings = Settings()
