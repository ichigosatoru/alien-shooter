import pygame.font
from pygame.sprite import Group
from ship import Ship
import pygame

class Scoreboard: 
    """A class to report scoring information."""
    def __init__(self, ai_game): 
        """Initialize scorekeeping attributes."""
        self.ai_game = ai_game
        self.screen = ai_game.screen 
        self.screen_rect = self.screen.get_rect() 
        self.settings = ai_game.settings 
        self.stats = ai_game.stats 

        # Font settings for scoring information
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        self.small_font = pygame.font.SysFont(None, 36)

        # Prepare the initial score images
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group()

        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def prep_score(self):
        """Turn the score into a rendered image."""
        #score_str = str(self.stats.score)
        rounded_score = round(self.stats.score, -1)
        score_str = f"score:{rounded_score:,}"
        self.score_image = self.font.render(score_str, True,
                                            self.text_color, self.settings.bg_color)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        scores = self.ai_game.high_scores_manager.get_high_scores()
        
        # Start with 5th place (lowest score)
        high_score = scores[-1]['score'] if scores else 0
        
        # Find which rank the player is trying to beat
        for score_entry in scores:
            if self.stats.score >= score_entry['score']:
                high_score = score_entry['score']
            else:
                break
        
        high_score = round(high_score, -1)
        high_score_str = f"hi score: {high_score:,}"
        self.high_score_image = self.font.render(high_score_str, True,
                                                self.text_color, self.settings.bg_color)

        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        """Check to see if there's a new high score."""
        scores = self.ai_game.high_scores_manager.get_high_scores()
        if scores:
            for score_entry in scores:
                if self.stats.score > score_entry['score'] and self.stats.high_score < score_entry['score']:
                    self.stats.high_score = score_entry['score']
                    self.prep_high_score()
                    break

    def prep_level(self): 
        """Turn the level into a rendered image."""
        level_str = str(self.stats.level)
        self.level_image = self.font.render("level:"+level_str, True,
                                            self.text_color, self.settings.bg_color)

        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10
    
    def show_score(self):
        """Draw scores, level, and ships to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
    
    def show_high_scores_screen(self):
        """Display the high scores screen."""
        self.screen.fill(self.settings.bg_color)
        
        # Title
        title_font = pygame.font.SysFont(None, 72)
        title_image = title_font.render("HIGH SCORES", True, (255, 255, 255))
        title_rect = title_image.get_rect()
        title_rect.centerx = self.screen_rect.centerx
        title_rect.top = 50
        self.screen.blit(title_image, title_rect)
        
        # High scores list
        y_position = 150
        for score_entry in self.ai_game.high_scores_manager.get_high_scores():
            score_text = f"{score_entry['rank']}. {score_entry['name']:<15} {score_entry['score']:>10,}"
            score_image = self.small_font.render(score_text, True, (255, 255, 255))
            score_rect = score_image.get_rect()
            score_rect.centerx = self.screen_rect.centerx
            score_rect.top = y_position
            self.screen.blit(score_image, score_rect)
            y_position += 60
        
        pygame.display.flip()
