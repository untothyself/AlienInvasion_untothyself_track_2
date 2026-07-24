from time import sleep

import pygame

from alien_fleet import AlienFleet
from arsenal import Arsenal
from button import Button
from game_stats import GameStats
from HUD import HUD
from settings import Settings
from ship import Ship


class AlienInvasion:
    """Manage the Alien Invasion game and its main loop."""

    def __init__(self) -> None:
        """Initialize pygame, the screen, game objects, and optional audio."""
        pygame.init()
        self.settings = Settings()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption(self.settings.name)

        self.bg = self._load_background()
        self.running: bool = True
        self.impact_sound: pygame.mixer.Sound | None = None
        self.laser_sound: pygame.mixer.Sound | None = None
        self._initialize_audio()

        self.arsenal = Arsenal(self)
        self.ship = Ship(self, self.arsenal)
        self.alien_fleet = AlienFleet(self)
        self.stats = GameStats(self)
        self.play_button = Button(self, "Play")
        self.hud = HUD(self)
        self.alien_fleet.create_fleet()

    def _load_background(self) -> pygame.Surface:
        """Load the background or create a plain fallback background."""
        size = (self.settings.screen_width, self.settings.screen_height)
        try:
            image = pygame.image.load(self.settings.bg_file).convert()
            return pygame.transform.scale(image, size)
        except (FileNotFoundError, pygame.error):
            image = pygame.Surface(size)
            image.fill(self.settings.bg_color)
            return image

    def _initialize_audio(self) -> None:
        """Load sounds when an audio device and sound files are available."""
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            self.impact_sound = pygame.mixer.Sound(self.settings.impact_sound)
            self.laser_sound = pygame.mixer.Sound(self.settings.laser_sound)
        except (FileNotFoundError, pygame.error):
            self.impact_sound = None
            self.laser_sound = None

    def run_game(self) -> None:
        """Run the main game loop."""
        while self.running:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self.alien_fleet.update_fleet()
                self._check_collisions()

            self._update_screen()
            self.clock.tick(self.settings.FPS)

    def _check_events(self) -> None:
        """Respond to keyboard, mouse, and window events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit_game()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_play_button(event.pos)

    def _check_play_button(self, mouse_pos: tuple[int, int]) -> None:
        """Start a fresh game when the inactive Play button is clicked."""
        if not self.play_button.check_clicked(mouse_pos) or self.stats.game_active:
            return

        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.ship.center_ship()
        self._reset_level(level_up=False)
        self.stats.game_active = True
        self.hud.update_scores()
        pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event: pygame.event.Event) -> None:
        """Respond to key presses."""
        if event.key == pygame.K_q:
            self._quit_game()
            return

        if not self.stats.game_active:
            return

        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            if self.ship.fire() and self.laser_sound is not None:
                self.laser_sound.play()

    def _check_keyup_events(self, event: pygame.event.Event) -> None:
        """Stop movement when an arrow key is released."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _update_screen(self) -> None:
        """Draw the current frame and make it visible."""
        self.screen.blit(self.bg, (0, 0))
        self.ship.draw()
        self.alien_fleet.draw()
        self.hud.draw_scores()

        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

    def _quit_game(self) -> None:
        """Close pygame and exit the program."""
        self.running = False
        pygame.quit()
        raise SystemExit

    def _ship_hit(self) -> None:
        """Remove one life, reset the level, or end the game."""
        self.stats.ships_left -= 1
        self.hud.check_high_score()

        if self.stats.ships_left > 0:
            self._reset_level(level_up=False)
            self.ship.center_ship()
            self.hud.update_scores()
            sleep(0.5)
            return

        self.stats.ships_left = 0
        self.stats.game_active = False
        self.arsenal.bullets.empty()
        self.ship.center_ship()
        self.hud.update_scores()
        pygame.mouse.set_visible(True)

    def _reset_level(self, level_up: bool = True) -> None:
        """Clear projectiles, rebuild the fleet, and optionally increase speed."""
        self.stats.max_score = max(self.stats.max_score, self.stats.score)
        self.hud.check_high_score()

        if level_up:
            self.settings.increase_difficulty()

        self.arsenal.bullets.empty()
        self.alien_fleet.fleet.empty()
        self.alien_fleet.fleet_direction = self.settings.fleet_direction
        self.alien_fleet.create_fleet()
        self.ship.center_ship()
        self.hud.update_scores()

    def _check_collisions(self) -> None:
        """Handle bullet, alien, ship, and screen-bottom collisions."""
        collisions = pygame.sprite.groupcollide(
            self.arsenal.bullets, self.alien_fleet.fleet, True, True
        )

        if collisions:
            if self.impact_sound is not None:
                self.impact_sound.play()
            destroyed_count = sum(len(aliens) for aliens in collisions.values())
            self.stats.score += destroyed_count * 10
            self.hud.update_scores()

        if self.alien_fleet.check_destroyed_status():
            self._reset_level(level_up=True)
            return

        ship_collided = any(
    self.ship.rect.colliderect(alien.rect)
    for alien in self.alien_fleet.fleet.sprites()
)

        if ship_collided:
            self._ship_hit()
        elif self.alien_fleet.check_fleet_bottom():
            self._ship_hit()


if __name__ == "__main__":
    AlienInvasion().run_game()