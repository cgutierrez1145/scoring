class GameStats:
    """Track statistics for Alien Invasion."""
    
    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings # initialize game settings
        self.reset_stats() # Initialize statistics that can change during the game.

        # Start game in an inactive state.
        self.game_active = False

        # High score should never be reset.
        self.high_score = 0
        
    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit # set lives based on settings
        self.score = 0 # set score to initially be 0
        self.level = 1 # set initial level to 1