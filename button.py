import pygame.font
 
class Button:
 
    def __init__(self, ai_game, msg):
        """Initialize button attributes."""
        self.screen = ai_game.screen # initialize screen
        self.screen_rect = self.screen.get_rect() # reference to set rect size 
        
        # Set the dimensions and properties of the button.
        self.width, self.height = 200, 90 # width and height in pixels of button
        self.button_color = (42,245,255) # green button
        self.text_color = (0, 0, 0) # White font color
        self.font = pygame.font.SysFont("comicsansms", 48) # set font
        
        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center # center button
        
        # The button message needs to be prepped only once.
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color,
                self.button_color) # draw message text "Play"
        self.msg_image_rect = self.msg_image.get_rect() # # wheer to draw image
        self.msg_image_rect.center = self.rect.center # center image on rect

    def draw_button(self):
        # Draw blank button and then draw message.
        self.screen.fill(self.button_color, self.rect) # drwa blank button
        self.screen.blit(self.msg_image, self.msg_image_rect) # add image/message to button