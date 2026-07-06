import pygame
from pygame.sprite import Sprite
from audio import *

MOST_LEFT = -0.5
MOST_RIGHT = 1273.0

class Ship(Sprite):
    """A class to manage the ship."""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and get its rect.
        self.image = pygame.image.load('D:\\DEREK\\PYTHON CODES\\alien shooter\\images\\ship.bmp')
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a float for the ship's exact horizontal position.
        self.x = float(self.rect.x)

        # Movement flag; start with a ship that's not moving.
        self.moving_right = False
        self.moving_left = False
        self.teleport_left = False
        self.teleport_right = False

        #teleport points
        self.teleport_points = 0
        
        # Speed boost attributes
        self.is_speed_boosted = False
        self.boost_start_time = 0
        self.normal_ship_speed = self.settings.ship_speed
        self.double_shot_active = False
        self.double_shot_start_time = 0

    def update(self):
        """Update the ship's position based on the movement flag."""
        # Check if speed boost has expired
        if self.is_speed_boosted:
            elapsed_time = pygame.time.get_ticks() - self.boost_start_time
            if elapsed_time >= self.settings.speed_boost_duration:
                self.is_speed_boosted = False
                self.settings.ship_speed = self.normal_ship_speed
        
        # Check if double shot has expired
        if self.double_shot_active:
            elapsed_time = pygame.time.get_ticks() - self.double_shot_start_time
            if elapsed_time >= self.settings.speed_boost_duration:
                self.double_shot_active = False
        
        #update the ship's x value not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed

        if self.moving_left and self.rect.left > 0:
           self.x -= self.settings.ship_speed

        if self.teleport_left:
            if self.teleport_points >= 1.0:
                self.x = MOST_LEFT
                sound_change_phase(event="teleport")
                self.teleport_points -= 1.0

        if self.teleport_right:
            if self.teleport_points >= 1.0:
                self.x = MOST_RIGHT
                sound_change_phase(event="teleport")
                self.teleport_points -= 1.0

        # Update rect object from self.x.
        self.rect.x = self.x

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
    
    def activate_speed_boost(self):
        """Activate speed boost for 5 seconds."""
        if not self.is_speed_boosted:
            self.is_speed_boosted = True
            self.boost_start_time = pygame.time.get_ticks()
            self.normal_ship_speed = self.settings.ship_speed
            self.settings.ship_speed *= self.settings.speed_boost_multiplier
    
    def activate_double_shot(self):
        """Activate double shot for 5 seconds."""
        if not self.double_shot_active:
            self.double_shot_active = True
            self.double_shot_start_time = pygame.time.get_ticks()
