from typing import TYPE_CHECKING

import pygame

from alien import Alien

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class AlienFleet:
    """Create, move, and inspect the alien fleet."""

    def __init__(self, ai_game: "AlienInvasion") -> None:
        """Initialize an empty alien fleet."""
        self.game = ai_game
        self.settings = ai_game.settings
        self.fleet = pygame.sprite.Group()
        self.fleet_direction: int = self.settings.fleet_direction

    def create_fleet(self) -> None:
        """Generate a centered grid of aliens."""
        self.fleet_direction = self.settings.fleet_direction
        fleet_width, fleet_height = self._calculate_fleet_size()
        x_offset, y_offset = self._calculate_offsets(
            fleet_width, fleet_height
        )
        self._create_rectangle_fleet(
            fleet_width, fleet_height, x_offset, y_offset
        )

    def _calculate_fleet_size(self) -> tuple[int, int]:
        """Calculate how many grid spaces fit in the top half."""
        width_count = max(
            3, self.settings.screen_width // self.settings.alien_w
        )
        height_count = max(
            3,
            (self.settings.screen_height // 2) // self.settings.alien_h,
        )

        # Odd counts keep the spaced fleet centered.
        if width_count % 2 == 0:
            width_count -= 1
        if height_count % 2 == 0:
            height_count -= 1

        return width_count, height_count

    def _calculate_offsets(
        self, fleet_width: int, fleet_height: int
    ) -> tuple[int, int]:
        """Calculate offsets that center the fleet."""
        horizontal_space = fleet_width * self.settings.alien_w
        x_offset = (
            self.settings.screen_width - horizontal_space
        ) // 2

        half_screen_height = self.settings.screen_height // 2
        vertical_space = fleet_height * self.settings.alien_h
        y_offset = (half_screen_height - vertical_space) // 2

        return x_offset, y_offset

    def _create_rectangle_fleet(
        self,
        fleet_width: int,
        fleet_height: int,
        x_offset: int,
        y_offset: int,
    ) -> None:
        """Place aliens in alternating grid spaces."""
        for row in range(1, fleet_height, 2):
            for column in range(1, fleet_width, 2):
                current_x = (
                    column * self.settings.alien_w + x_offset
                )
                current_y = row * self.settings.alien_h + y_offset
                self.fleet.add(Alien(self, current_x, current_y))

    def update_fleet(self) -> None:
        """Move the fleet and reverse it at a screen edge."""
        if self._check_fleet_edges():
            self._drop_fleet()
            self.fleet_direction *= -1

        self.fleet.update()

    def _check_fleet_edges(self) -> bool:
        """Return True when any alien reaches a side edge."""
        return any(
            alien.check_edges() for alien in self.fleet.sprites()
        )

    def _drop_fleet(self) -> None:
        """Move every alien downward."""
        for alien in self.fleet.sprites():
            alien.y += self.settings.fleet_drop_speed
            alien.rect.y = int(alien.y)

    def draw(self) -> None:
        """Draw every alien in the fleet."""
        self.fleet.draw(self.game.screen)

    def check_fleet_bottom(self) -> bool:
        """Return True when an alien reaches the screen bottom."""
        return any(
            alien.rect.bottom >= self.settings.screen_height
            for alien in self.fleet.sprites()
        )

    def check_destroyed_status(self) -> bool:
        """Return True when no aliens remain."""
        return len(self.fleet) == 0