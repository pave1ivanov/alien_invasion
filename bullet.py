import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """ Bullets management class"""

    def __init__(self, ai_game):
        """ Create bullets object for the current ship position """
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet in (0, 0) and assign the correct position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Save the center Y-axis position of the bullet using a float value
        self.y = float(self.rect.y)

    def update(self):
        """ Move a bullet on the screen """
        # change the float value of the position of the bullet
        self.y -= self.settings.bullet_speed_factor

        # assign the position value to the bullet
        self.rect.y = self.y

    def draw_bullet(self):
        """ Display a bullet """
        pygame.draw.rect(self.screen, self.color, self.rect)

