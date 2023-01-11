import pygame.font


class Button:
    def __init__(self, ai_game, msg):
        """ Initialize the button attributes """
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # specify the size and characteristics of the button
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = ai_game.settings.bg_color
        self.font = pygame.font.SysFont(None, 48)

        # create the rect of the button and center it on the screen
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # create text of the button
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """ Convert text to a rect and center it """
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """ Create a button and place text into it """
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

