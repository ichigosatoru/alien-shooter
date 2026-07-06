import pygame
from pygame.locals import *
music_path = "C:\\Users\\derek\\Music\\music\\"
effect_path = "D:\\DEREK\\PYTHON CODES\\LEARNING_POKEMON\\Python-Monsters-main\\audio\\"
level_flag_keeping_stages_sounds_uptodate = 0


SOUNDS = {
    'main': "Bachira Meguru (Blue Lock UK Rap) [Brazillian Funk].mp3",

    'alien-ship-collision':   'splash.wav',
    'bullet-alien-collision': 'notice.wav',
    'new level':              'green.wav',
    'new high score':         'scratch.mp3',
    'teleport':               'ice.mp3'

    }


class Settings:
    """A class to store all settings for AlienInvasion"""
    def __init__(self):
        """Initialize the game's static settings."""
        #screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (72,63,204)#it is the value taken from paint
        
        


        #ship's settings
        self.ship_speed = 2.0#moves by 1.5 pixels
        self.ship_limit = 0

        # Bullet settings
        self.bullet_speed = 3.5#travels slightly faster than ship
        self.bullet_width = 5
        self.bullet_height = 10
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5

        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 5

        # How quickly the game speeds up
        self.speedup_scale = 1.3

        # How quickly the alien point values increase
        self.score_scale = 1.5

        #teleport number 
        self.teleport_points = 0
        
        # Speed boost settings
        self.speed_boost_multiplier = 2.0  # Ship moves 2x faster when boosted
        self.speed_boost_duration = 5000  # 5 seconds in milliseconds
        
        # Special alien settings
        self.special_alien_spawn_level = 5  # Special aliens appear from level 5
        self.special_alien_spawn_chance = 10  # 10% chance (1 in 10)

        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 1.5
        self.bullet_speed = 2.5
        self.alien_speed = 1.5

        # Scoring settings
        self.alien_points = 50

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
     
    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
