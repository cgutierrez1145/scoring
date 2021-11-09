import pygame
 
from pygame.sprite import Sprite
 
class Ship(Sprite):
    """A class to manage the ship."""
 
    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen # initialize screen
        self.settings = ai_game.settings # initialize settings
        self.screen_rect = ai_game.screen.get_rect() # reference to rect for ship

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp') # image of ship
        self.rect = self.image.get_rect() # get rect to load image

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal value for the ship's horizontal position.
        self.x = float(self.rect.x)

        # Movement flags
        self.moving_right = False # not moving right
        self.moving_left = False # not moving left

    def update(self):
        """Update the ship's position based on movement flags."""
        # Update the ship's x value, not the rect.
        # if inbounds and moving right
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed # move right
        # if inbounds and moving left
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed # move left

        # Update rect object from self.x.
        self.rect.x = self.x

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect) # draw ship from list of images

    def center_ship(self):
        """Center the ship on the screen."""
        # reference middle bottom of game rect
        self.rect.midbottom = self.screen_rect.midbottom 
        self.x = float(self.rect.x) # set ship at middle bottom
