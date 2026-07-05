import pygame.font
from tkinter import simpledialog, Tk
import pygame

class GameOverScreen:
    """Display game over screen and handle name input."""
    
    def __init__(self, ai_game):
        """Initialize game over screen."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        
        # Font settings
        self.font_large = pygame.font.SysFont(None, 72)
        self.font_medium = pygame.font.SysFont(None, 48)
        self.font_small = pygame.font.SysFont(None, 36)
    
    def display_game_over(self):
        """Display game over screen and check for high score."""
        self.screen.fill(self.settings.bg_color)
        
        # Game Over text
        game_over_image = self.font_large.render("GAME OVER", True, (255, 0, 0))
        game_over_rect = game_over_image.get_rect()
        game_over_rect.centerx = self.screen_rect.centerx
        game_over_rect.centery = self.screen_rect.centery - 150
        self.screen.blit(game_over_image, game_over_rect)
        
        # Final score
        final_score = round(self.stats.score, -1)
        score_text = f"Final Score: {final_score:,}"
        score_image = self.font_medium.render(score_text, True, (255, 255, 255))
        score_rect = score_image.get_rect()
        score_rect.centerx = self.screen_rect.centerx
        score_rect.top = game_over_rect.bottom + 50
        self.screen.blit(score_image, score_rect)
        
        # Check if it's a high score
        is_high_score = self.ai_game.high_scores_manager.is_high_score(self.stats.score)
        
        if is_high_score:
            # Get player name
            pygame.display.flip()
            player_name = self.get_player_name()
            
            if player_name:
                rank = self.ai_game.high_scores_manager.get_rank(self.stats.score)
                self.ai_game.high_scores_manager.add_score(player_name, self.stats.score)
                
                # Display new high score message
                self.screen.fill(self.settings.bg_color)
                self.screen.blit(game_over_image, game_over_rect)
                self.screen.blit(score_image, score_rect)
                
                congrats_text = f"NEW HIGH SCORE! Rank #{rank}"
                congrats_image = self.font_medium.render(congrats_text, True, (0, 255, 0))
                congrats_rect = congrats_image.get_rect()
                congrats_rect.centerx = self.screen_rect.centerx
                congrats_rect.top = score_rect.bottom + 40
                self.screen.blit(congrats_image, congrats_rect)
                
                name_text = f"Player: {player_name.upper()}"
                name_image = self.font_small.render(name_text, True, (255, 255, 255))
                name_rect = name_image.get_rect()
                name_rect.centerx = self.screen_rect.centerx
                name_rect.top = congrats_rect.bottom + 20
                self.screen.blit(name_image, name_rect)
        else:
            # Not a high score
            not_high_score_text = "Not a High Score"
            not_high_score_image = self.font_small.render(not_high_score_text, True, (200, 200, 200))
            not_high_score_rect = not_high_score_image.get_rect()
            not_high_score_rect.centerx = self.screen_rect.centerx
            not_high_score_rect.top = score_rect.bottom + 40
            self.screen.blit(not_high_score_image, not_high_score_rect)
        
        # Instructions
        instruction_text = "Click PLAY button to try again"
        instruction_image = self.font_small.render(instruction_text, True, (255, 255, 255))
        instruction_rect = instruction_image.get_rect()
        instruction_rect.centerx = self.screen_rect.centerx
        instruction_rect.bottom = self.screen_rect.bottom - 50
        self.screen.blit(instruction_image, instruction_rect)
        
        pygame.display.flip()
    
    def get_player_name(self):
        """Get player name using tkinter dialog."""
        root = Tk()
        root.withdraw()  # Hide the main tkinter window
        
        player_name = simpledialog.askstring(
            "High Score!",
            "Enter your name (max 15 characters):",
            parent=root
        )
        
        root.destroy()
        
        if player_name:
            return player_name[:15]  # Limit to 15 characters
        return None
