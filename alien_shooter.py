import math
import random
import timeit
from tkinter import messagebox
import sys
from pygame.locals import *
from time import *

import pygame, sys

from settings import *
from settings import level_flag_keeping_stages_sounds_uptodate as lvl
from game_stats import GameStats
from scoreboard import Scoreboard
from buttons import Button
from ship import Ship
from bullets import Bullet
from alien import Alien
from audio import *
from highscores import HighScoresManager
from game_over_screen import GameOverScreen
import json
import os



class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()#controlling frame rate
        self.settings = Settings()
        
        # Initialize high scores manager
        self.high_scores_manager = HighScoresManager()
        self.game_over_screen = None

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))


        #self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Alien Invasion")

        # Create an instance to store game statistics, scoreboard, an instance of ship and bullets.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        # Load high score from JSON file
        self.stats.high_score = self.high_scores_manager.get_high_scores()[0]['score'] if self.high_scores_manager.get_high_scores() else 0
        self.game_over_screen = GameOverScreen(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # Set the background color.
        self.bg_color = (230,230,230)#RGB % of red green blue

        # Start Alien Invasion in an inactive state.
        self.game_active = False
        
        # Make the Play button.
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start the main loop for the game."""
        # self.stats.high_score = self._load_hi_score()
        while True:
            # Watch for keyboard and mouse events.
            self.check_events()

            if self.game_active:
                self.ship.update()

                self.bullets.update()

                self._update_bullets()

                self._update_aliens()

            self.update_screen()

            # Redraw the screen during each pass through the loop.
            self.screen.fill(self.bg_color)
            
            # Make the most recently drawn screen visible.
            self.clock.tick(60)#try different values

    def check_events(self):
        for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()

                    elif event.type == pygame.KEYDOWN:
                        self._check_keydown_events(event)

                    elif event.type == pygame.KEYUP:
                        self._check_keyup_events(event)

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        self._check_play_button(mouse_pos)

    def _check_keydown_events(self,event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            # Move the ship to the right.
            self.ship.rect.x += 1
            self.ship.moving_right = True
            
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True

        elif event.key == pygame.K_q:
            sys.exit()

        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

        elif event.key == pygame.K_KP1:
            self.ship.teleport_left = True
            
        elif event.key == pygame.K_KP3:
            self.ship.teleport_right = True

    def _check_keyup_events(self,event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False

        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

        elif event.key == pygame.K_KP1:
            self.ship.teleport_left = False

        elif event.key == pygame.K_KP3:
            self.ship.teleport_right = False
        

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()

            # Reset the game statistics.
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True

            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

        # Hide the mouse cursor.
        pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            
            # If double shot is active, fire a second bullet offset
            if self.ship.double_shot_active and len(self.bullets) < self.settings.bullets_allowed:
                new_bullet2 = Bullet(self)
                new_bullet2.rect.x -= 10  # Offset to the left
                self.bullets.add(new_bullet2)

    def update_screen(self):
        #update img to the screen and flip into the new screen
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.ship.blitme()

        self.aliens.draw(self.screen)#display alien

        # Draw the score information. 
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.game_active:#so button appear only if inactive
            self.play_button.draw_button()

        pygame.display.flip()

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""

        if self.stats.ships_left > 0:
           # Decrement ships_left, and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            #pause
            sleep(0.5)

        else:
            sound_change_phase("alien-ship-collision", True)
            self.game_active = False
            pygame.mouse.set_visible(True)
            
            # Display game over screen with high scores
            self.game_over_screen.display_game_over()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        # Check for any bullets that have hit aliens.
        # If so, get rid of the bullet and the alien.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            sound_change_phase(event="bullet-alien-collision")
            for aliens in collisions.values(): 
                for alien in aliens:
                    if alien._is_special:
                        self.boost_ship()
                        self.ship.activate_speed_boost()  # Activate speed boost
                        self.ship.activate_double_shot()  # Activate double shot
                        
                    if not alien._is_special:
                        continue  

                self.stats.score += self.settings.alien_points * len(aliens)
                if self.stats.score > self.stats.high_score:
                    sound_change_phase(event="new high score")
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            sound_change_phase(event="new level")
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()

    def boost_ship(self):
        self.ship.teleport_points += 0.5

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        """Check if the fleet is at an edge, then update positions."""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_fleet(self):
       # Create an alien and keep adding aliens until there's no room left.
        # Spacing between aliens is one alien width and one alien height.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        current_x, current_y = alien_width, alien_height
        
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):#As long as there's at least two alien widths' worth
                # Only spawn special aliens from level 5 onwards
                if self.stats.level >= self.settings.special_alien_spawn_level:
                    self.choice = random.randint(0, self.settings.special_alien_spawn_chance)
                    if self.choice == 0:  # 10% chance (1 in 10)
                        self._create_alien(current_x, current_y, True)
                    else:
                        self._create_alien(current_x, current_y)
                else:
                    # No special aliens before level 5
                    self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # Finished a row; reset x value, and increment y value.
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position, is_special=False):
        """Create an alien and place it in the fleet."""
        new_alien = Alien(self, is_special)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)
        
    
         

    
#main program
if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()

    #RE ENABLE TO HAVE BACKGROUND SOUND
    # try:
    #     soundObj = pygame.mixer.Sound(music_path+SOUNDS['main'])
    #     soundObj.set_volume(0.63)
    # except KeyError as error:
    #     messagebox.showerror(title=error, message="VALUES FOR MAIN AUDIO NOT FOUND!!!!")
    # finally:
    #     pass
    ai.run_game()
