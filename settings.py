class Settings:
    """ Alien Invasion game settings"""

    def __init__(self):
        """ Initialize static settings of the game"""
        # screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (10, 29, 44)

        # ship settings
        self.ship_limit = 3

        # bullet settings
        self.bullet_width = 3
        self.bullet_height = 20
        self.bullet_color = (255, 99, 71)
        self.bullets_allowed = 5

        # aliens settings
        self.fleet_drop_speed = 10

        # speed up factor after a fleet is destroyed
        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """ Initialize settings which change during a game """
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3.0
        self.alien_speed_factor = 1.8
        self.alien_points = 50

        self.feet_direction = 1

    def increase_speed(self):
        """ Increase speed settings """
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        # Increase amount of points for an alien hit as well
        self.alien_points = int(self.alien_points * self.score_scale)
