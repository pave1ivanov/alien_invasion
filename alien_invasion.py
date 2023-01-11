import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from alien import Alien
from bullet import Bullet
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """ Class for managing resources and game behaviour """

    def __init__(self):
        """ Initialize the game and create game resources """
        pygame.init()
        self.settings = Settings()

        # Set screen size
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('Alien Invasion')

        # Load resources
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        # Create a fleet of aliens
        self._create_fleet()

        # Create the play button
        self.play_button = Button(self, 'Play')

    def run_game(self):
        """ Start the main game loop """
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events(self):
        """ Watch keyboard and mouse events """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """ Starts a new game when the Play button is pressed"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset game speed
            self.settings.initialize_dynamic_settings()

            # Reset stats for a new game
            self.stats.reset_stats()
            self.stats.game_active = True

            # Reset game resources
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Hide mouse
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """ Events when buttons are pressed """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """ Events when buttons are released """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _create_fleet(self):
        """ Create aliens fleet """
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (10 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Count number of rows to fit vertically
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - (10 * alien_height) - ship_height
        number_of_rows = available_space_y // (2 * alien_height)

        for row_number in range(number_of_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """ Create an alien and place it in a row """
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """ Trigger the fleet direction change if any alien reaches an edge """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _check_aliens_bottom(self):
        """ Check if aliens reach bottom of the screen """
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Act like the ship has been hit
                self._ship_hit()
                break

    def _change_fleet_direction(self):
        """ Drop the fleet and change its direction """
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.feet_direction *= -1

    def _fire_bullet(self):
        """ Create new bullet and add it to the bullets group """
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """ Update bullets position and delete off-screen bullets"""
        self.bullets.update()

        # Delete out off-screen bullets
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """ Manage collisions of bullets and aliens """
        # Check if a bullet hits an aliens, delete both
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        # Update score according to the number of alien hits
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.sb.prep_score()
                self.sb.check_high_score()

        # Create new fleet when all aliens are killed
        if not self.aliens:
            # Delete all bullets
            self.bullets.empty()
            # Crate new fleet
            self._create_fleet()
            # Increase game speed
            self.settings.increase_speed()
            # Increase the level
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """ Updates positions of all aliens in the fleet """
        self._check_fleet_edges()
        self.aliens.update()

        # Check alien - ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Check if aliens reached the bottom
        self._check_aliens_bottom()

    def _ship_hit(self):
        """ Manage ship-alien collision """
        # Decrease amount of ships left and update scoreboard
        self.stats.ships_left -= 1
        self.sb.prep_ships()

        # Delete all aliens and bullets
        self.aliens.empty()
        self.bullets.empty()

        # Create a new fleet and center there are spare ships left
        if self.stats.ships_left > 0:
            self._create_fleet()
            self.ship.center_ship()
            sleep(1)
        else:
            # If no ships left stop the game
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _update_screen(self):
        """ Create and display a screen """
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Show scoreboard
        self.sb.show_score()

        # If game is inactive show the Play button
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    # Create and start an instance of the game
    ai = AlienInvasion()
    ai.run_game()
