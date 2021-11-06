import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init() # initialize all pygame modules
        self.settings = Settings() # Initialize a settings object for the current game

        # Initialize screen for display set_mode(0,0) sets best possible match
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        # set screen width based on screen dimensions
        self.settings.screen_width = self.screen.get_rect().width

        # set screen width based on screen dimensions
        self.settings.screen_height = self.screen.get_rect().height

        # set title of display (Screen)
        pygame.display.set_caption("Alien Invasion")

        # Create a GameStats instance to store game statistics,
        self.stats = GameStats(self)
        self.sb = Scoreboard(self) # Create a scoreboard.
        self.ship = Ship(self) # create a Ship instance

        # load alien and ship bitmap images
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet() # create a fleet of Instances of alien objects

        # Make the Play button.
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events() # check for keyboard or mouse presses

            if self.stats.game_active: # confirm game is running
                self.ship.update() # update ship instance based on user input
                self._update_bullets() # update bullet/s location based on user input
                self._update_aliens() # update alien/s location

            self._update_screen() # redraw the screen

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get(): # get all messages and remove from the queue
            if event.type == pygame.QUIT: # reads exit condition
                sys.exit() # exit game
            elif event.type == pygame.KEYDOWN: # if a key on keyboard is pressed
                self._check_keydown_events(event) # respond to keypresses
            elif event.type == pygame.KEYUP: # check if a key is released
                self._check_keyup_events(event) # respond to key releases
            elif event.type == pygame.MOUSEBUTTONDOWN: # check if mouse button is pressed
                mouse_pos = pygame.mouse.get_pos() # get position of mouse cursor
                self._check_play_button(mouse_pos)  # respond to mouse button pressed

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        # set to true if play button is clicked
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        # play button is clicked and another game is not active
        if button_clicked and not self.stats.game_active: 
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()
            
            self.stats.reset_stats() # Reset the game statistics.
            self.stats.game_active = True # set game to active
            self.sb.prep_score() # Turn the score into a rendered image.
            self.sb.prep_level() # turn the level into a rendered image
            self.sb.prep_ships() # show how many ships are left

            # Get rid of any remaining aliens and bullets.
            self.aliens.empty() # remove all alien instances from game screen
            self.bullets.empty() # remove all bullet instances from game screen
            
            # Create a new fleet and center the ship.
            self._create_fleet()  # create a fleet of Instances of alien objects
            self.ship.center_ship() # Center the ship on the screen

            pygame.mouse.set_visible(False) # Hide the mouse cursor.

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT: # if right arrow pressed
            self.ship.moving_right = True # move ship right
        elif event.key == pygame.K_LEFT: # if left arrow pressed
            self.ship.moving_left = True # move ship left
        elif event.key == pygame.K_q: # if q button pressed
            sys.exit() # exit game
        elif event.key == pygame.K_SPACE:  # if space button pressed
            self._fire_bullet() # Create a new bullet and add it to the bullets group.

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT: # right arrow released
            self.ship.moving_right = False # stop moving right
        elif event.key == pygame.K_LEFT: # left arrow released
            self.ship.moving_left = False # stop moving left

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        # ensure max number of bullets is not surpassed
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self) # Instantiate new bullet
            self.bullets.add(new_bullet) # Add new bullet to list of bullets

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy(): # go through all bullets
            if bullet.rect.bottom <= 0: # if bullet is out of range
                 self.bullets.remove(bullet) # remove bullet from list of all bullets

        self._check_bullet_alien_collisions() # Respond to bullet-alien collisions

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        # Find all sprites that collide between bullets and aliens (doKill arguments = True).
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions: # if collision occurs
            for aliens in collisions.values(): # go through each alien that collided in aliens list
                self.stats.score += self.settings.alien_points * len(aliens) # increase score
            self.sb.prep_score() # Turn the score into a rendered image.
            self.sb.check_high_score() # Check to see if there's a new high score

        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty() # empty bullets list (remove all projectiles)
            self._create_fleet() # create a fleet of Instances of alien objects
            self.settings.increase_speed() # Increase speed settings and alien point values.

            self.stats.level += 1 # Increase level.
            self.sb.prep_level()  # turn the level into a rendered image

    def _update_aliens(self):
        """
        Check if the fleet is at an edge,
          then update the positions of all aliens in the fleet.
        """
        self._check_fleet_edges() # Respond appropriately if any aliens have reached an edge.
        self.aliens.update() # update alien positions

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit() # Respond to the ship being hit by an alien

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom() # Check if any aliens have reached the bottom of the screen.

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect() # reference to screen
        # for each alien bitmap image
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom: # if alien is out of bounds
                # Treat this the same as if the ship got hit.
                self._ship_hit() # Respond to the ship being hit by an alien
                break # exit loop

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        # livews are still remaining
        if self.stats.ships_left > 0:
            # Decrement ships_left, and update scoreboard.
            self.stats.ships_left -= 1 # decrement number of lilves remaining
            self.sb.prep_ships()  # Show how many ships are left.
            
            # Get rid of any remaining aliens and bullets.
            self.aliens.empty() # remove remaining aliens
            self.bullets.empty() # remove remaining bullets
            
            # Create a new fleet and center the ship.
            self._create_fleet() # create a fleet of Instances of alien objects
            self.ship.center_ship() # Center the ship on the screen
            
            # Pause.
            sleep(0.5) # sleep for half a second
        else: # no lives remaining
            self.stats.game_active = False # set game inactive
            pygame.mouse.set_visible(True) # set mouse pointer to visible

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self) # Instantiate alien 
        alien_width, alien_height = alien.rect.size # Set alien size
        # space to left and right of aliens
        available_space_x = self.settings.screen_width - (2 * alien_width)
        # number of aliens per row (Integer value)
        number_aliens_x = available_space_x // (2 * alien_width)
        
        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height # determine size of ship bmp
        # vertical space for aliens
        available_space_y = (self.settings.screen_height -
                                (3 * alien_height) - ship_height)
        # Number of rows [Column height] (Integer value)                      
        number_rows = available_space_y // (2 * alien_height)
        
        # Create the full fleet of aliens.
        for row_number in range(number_rows): # go through each row of aliens
            for alien_number in range(number_aliens_x): # each alien in current row
                # Create an alien and place it in the row.
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""
        alien = Alien(self) # Instantiate alien
        alien_width, alien_height = alien.rect.size # Set alien size
        # set alien horizontal location
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x # set alien horizontal coordinates
        # set alien vertical coordinates
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien) # add current alien to list of aliens

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites(): # travers list of alien bmp images
            if alien.check_edges(): # if at edge of screen
                # Drop the entire fleet and change the fleet's direction
                self._change_fleet_direction()
                break # exit loop
            
    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():  # travers list of alien bmp images
            alien.rect.y += self.settings.fleet_drop_speed # reduce y coordinates
        # inverse fleet direction to negative of current value
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color) # paint screen to bg_color
        self.ship.blitme() # Draw the ship at its current location.
        for bullet in self.bullets.sprites(): # traverse list of bullet bmp images
            bullet.draw_bullet() # Draw the bullet to the screen.
        self.aliens.draw(self.screen) # draw aliens to screen

        # Draw the score information.
        self.sb.show_score() # Draw scores, level, and ships to the screen.

        # Draw the play button if the game is inactive.
        if not self.stats.game_active: # if game not active
            self.play_button.draw_button() # draw play button

        pygame.display.flip() # Update the full display Surface to the screen


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion() # instantiate game AI
    ai.run_game() # start the main game loop
