class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width = 1200 # set game width to 1200 px
        self.screen_height = 800 # set game height to 800 px
        self.bg_color = (45, 45, 45) # set game Background-color to nearly white

        # Ship settings
        self.ship_limit = 3 # number of lives

        # Bullet settings
        self.bullet_width = 4 # width of projectile in pixels
        self.bullet_height = 30 # height of projectile in pixels
        self.bullet_color = (42,245,255) # color of projectile (red)
        self.bullets_allowed = 5 # number of bullets allowed at any one point in time

        # Alien settings
        self.fleet_drop_speed = 6 # speed that aliens move downward

        # How quickly the game speeds up
        self.speedup_scale = 1.4

        # How quickly the alien point values increase
        self.score_scale = 1.4

        self.initialize_dynamic_settings() # set additional settings

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 1.5 # speed ship moves left and right
        self.bullet_speed = 2.0 # vertical speed of projectile 
        self.alien_speed = 0.8 # seed aliens move toward target

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale # increse ship speed
        self.bullet_speed *= self.speedup_scale # increase projectile speed
        self.alien_speed *= self.speedup_scale # increase alien speed

        self.alien_points = int(self.alien_points * self.score_scale) # increase points granted
