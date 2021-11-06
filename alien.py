import pygame
from pygame.sprite import Sprite
 
class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""
        super().__init__() # use parent class __init__
        self.screen = ai_game.screen # Initialize screen
        self.settings = ai_game.settings # Initialize settings

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load('images/alien.bmp') # set image
        self.rect = self.image.get_rect() # set image coordinates

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width # Set alien horixontal coordinates
        self.rect.y = self.rect.height # Set alien vertical coordinates

        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect() # get screen
        # check distance from edges
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True # at edge of screen

    def update(self):
        """Move the alien right or left."""
        # direction and speed
        self.x += (self.settings.alien_speed *
                        self.settings.fleet_direction)
        self.rect.x = self.x # set direction and speed
