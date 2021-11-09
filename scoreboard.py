import pygame.font
from pygame.sprite import Group
 
from ship import Ship

class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, ai_game):
        """Initialize scorekeeping attributes."""
        self.ai_game = ai_game # initialize game AI
        self.screen = ai_game.screen # initialize game screen
        self.screen_rect = self.screen.get_rect() # init game coordinates
        self.settings = ai_game.settings # init game settings
        self.stats = ai_game.stats # initialize game stats
        
        # Font settings for scoring information.
        self.text_color = (42,245,255) # set scoreboard text color (bluish)
        self.font = pygame.font.SysFont("comicsansms", 48) # set font size

        # Prepare the initial score images.
        self.prep_score() # Turn the score into a rendered image.
        self.prep_high_score() # Turn the high score into a rendered image.
        self.prep_level() # Turn the level into a rendered image
        self.prep_ships() # Show how many ships are left.

    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = round(self.stats.score, -1) # rounds removing one decimal point
        score_str = "{:,}".format(rounded_score) # format score and set as string
        # draw score to screen
        self.score_image = self.font.render(score_str, True,
                self.text_color, self.settings.bg_color)
        
        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect() # Set score coordinates
        # set score text coordinates 20 px from right
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20 # set score text coordinates 20 px from top

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = round(self.stats.high_score, -1) # rounds removing one decimal point
        high_score_str = "{:,}".format(high_score) # format high_score and set as string
        # draw high_score to screen
        self.high_score_image = self.font.render(high_score_str, True,
                self.text_color, self.settings.bg_color)
            
        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()  # Set score coordinates
        self.high_score_rect.centerx = self.screen_rect.centerx # set coord to center horizontally
        self.high_score_rect.top = self.score_rect.top # set coord to top of screen

    def prep_level(self):
        """Turn the level into a rendered image."""
        level_str = str(self.stats.level) # string representing level num
        # draw string to screen for level number
        self.level_image = self.font.render(level_str, True,
                self.text_color, self.settings.bg_color)
    
        # Position the level below the score.
        self.level_rect = self.level_image.get_rect() # set coordinates
        self.level_rect.right = self.score_rect.right # set level to right of screen
        self.level_rect.top = self.score_rect.bottom + 10 # set level 10 px from top

    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group() # A container class to hold and manage multiple Sprite objects.
        for ship_number in range(self.stats.ships_left): # each ship(life) still left
            ship = Ship(self.ai_game) # instantiate ship
            # draw next ship (life) image 
            ship.rect.x = 10 + ship_number * ship.rect.width 
            ship.rect.y = 10 # set ship 10 px from top
            self.ships.add(ship) # add ship to ships

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score: # if current score is greater than high_score
            self.stats.high_score = self.stats.score # set high score to current score
            self.prep_high_score() # Turn the high score into a rendered image.

    def show_score(self):
        """Draw scores, level, and ships to the screen."""
        self.screen.blit(self.score_image, self.score_rect) # draw score
        self.screen.blit(self.high_score_image, self.high_score_rect) # draw high score
        self.screen.blit(self.level_image, self.level_rect) # draw level number
        self.ships.draw(self.screen) # draw ships(lives)
