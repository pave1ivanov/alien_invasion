import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """ Alien management class """

    def __init__(self, ai_game):
        """ Initialize an alien and set its initial position """
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load image and set a rectangle
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Create an alien in the top-left corner
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Save center X-axis position of the alien using a float value
        self.x = float(self.rect.x)

    def check_edges(self):
        """ Returns True if an alien is at the screen edge """
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """ Move an alien according to the fleet direction and speed """
        self.x += self.settings.alien_speed_factor * self.settings.feet_direction
        self.rect.x = self.x


