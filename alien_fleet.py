"""
Program: The Hollow Watch - Track 2
Author: Abass Hassan
Purpose: Creates, moves, and manages the custom wedge enemy fleet.
Starter Code: Based on the Alien Invasion starter repository:
https://github.com/RedBeard41/alien_Invasion_starter.git
Date: July 30, 2026
"""

from typing import TYPE_CHECKING

import pygame

from alien import Alien

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class AlienFleet:
    """Create, move, draw, and inspect the custom enemy fleet."""

    def __init__(self, ai_game: "AlienInvasion") -> None:
        """Initialize an empty enemy fleet and its movement direction."""
        self.game = ai_game
        self.settings = ai_game.settings
        self.fleet = pygame.sprite.Group()
        self.fleet_direction: int = self.settings.fleet_direction

    def create_fleet(self) -> None:
        """Clear the old fleet and generate a centered wedge formation."""
        self.fleet.empty()
        self.fleet_direction = self.settings.fleet_direction
        self._create_wedge_fleet()

    def _create_wedge_fleet(self) -> None:
        """Place enemies in rows that widen into a triangular wedge."""
        row_counts = (1, 3, 5, 7, 9)

        horizontal_spacing = self.settings.alien_w + 24
        vertical_spacing = self.settings.alien_h + 18

        center_x = self.settings.screen_width // 2
        starting_y = 80

        for row_index, alien_count in enumerate(row_counts):
            row_width = (
                alien_count * self.settings.alien_w
                + (alien_count - 1) * 24
            )

            starting_x = center_x - row_width // 2
            current_y = starting_y + row_index * vertical_spacing

            for column_index in range(alien_count):
                current_x = (
                    starting_x
                    + column_index * horizontal_spacing
                )

                alien = Alien(
                    self,
                    float(current_x),
                    float(current_y),
                )

                self.fleet.add(alien)

    def update_fleet(self) -> None:
        """Move the fleet and reverse it after reaching a screen edge."""
        if self._check_fleet_edges():
            self._drop_fleet()
            self.fleet_direction *= -1

        self.fleet.update()

    def _check_fleet_edges(self) -> bool:
        """Return True when any enemy reaches a horizontal screen edge."""
        return any(
            alien.check_edges()
            for alien in self.fleet.sprites()
        )

    def _drop_fleet(self) -> None:
        """Move every enemy downward after the fleet reaches an edge."""
        for alien in self.fleet.sprites():
            alien.y += self.settings.fleet_drop_speed
            alien.rect.y = int(alien.y)

    def draw(self) -> None:
        """Draw every active enemy on the game screen."""
        self.fleet.draw(self.game.screen)

    def check_fleet_bottom(self) -> bool:
        """Return True when any enemy reaches the screen bottom."""
        return any(
            alien.rect.bottom >= self.settings.screen_height
            for alien in self.fleet.sprites()
        )

    def check_destroyed_status(self) -> bool:
        """Return True when the player has destroyed every enemy."""
        return len(self.fleet) == 0