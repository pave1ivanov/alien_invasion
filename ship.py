import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """ Ship management class """

    def __init__(self, ai_game):
        """ Initialize a ship and set its initial position """
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship image and create a rectangle
        self.image = pygame.image.load('images/ship3.png')
        self.rect = self.image.get_rect()

        # Initial position in the middle of the bottom
        self.rect.midbottom = self.screen_rect.midbottom

        # Save center X-axis position of the ship using a float value
        self.x = float(self.rect.x)

        # Movement flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """ Update the ship position recording to the flag"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed_factor

        # Assign float position to the ship
        self.rect.x = self.x

    def blitme(self):
        """ Create a ship in the current position"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """ Center the ship on the screen """
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
