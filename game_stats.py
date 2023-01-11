class GameStats:
    """ Alien Invasion game statistics """

    def __init__(self, ai_game):
        # initialize statistics
        self.settings = ai_game.settings
        self.reset_stats()

        # the game starts inactive
        self.game_active = False

        self.high_score = 0

    def reset_stats(self):
        """ Reset statistic for each new game """
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
