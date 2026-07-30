"""
Program: The Hollow Watch - Track 2
Author: Abass Hassan
Purpose: Manages the Gothic watchman, movement, and projectile firing.
Starter Code: Based on the Alien Invasion starter repository:
https://github.com/RedBeard41/alien_Invasion_starter.git
Date: July 26, 2026
"""
from typing import TYPE_CHECKING

import pygame
from pygame.sprite import Sprite

from arsenal import Arsenal

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class Ship(Sprite):
    """Manage the player's watchman character."""

    def __init__(
        self,
        ai_game: "AlienInvasion",
        arsenal: Arsenal,
    ) -> None:
        """Initialize the watchman at the bottom center of the screen."""
        super().__init__()

        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.boundaries = self.screen.get_rect()
        self.arsenal = arsenal

        self.image = self._load_image()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.midbottom = self.boundaries.midbottom

        self.moving_right: bool = False
        self.moving_left: bool = False
        self.x: float = float(self.rect.x)

    def _load_image(self) -> pygame.Surface:
        """Load the watchman image or create a visible fallback shape."""
        size = (
            self.settings.ship_width,
            self.settings.ship_height,
        )

        try:
            image = pygame.image.load(
                self.settings.ship_file
            ).convert_alpha()

            return pygame.transform.scale(
                image,
                size,
            )

        except (FileNotFoundError, pygame.error):
            fallback_image = pygame.Surface(
                size,
                pygame.SRCALPHA,
            )

            pygame.draw.rect(
                fallback_image,
                self.settings.ship_color,
                fallback_image.get_rect(),
                border_radius=8,
            )

            return fallback_image

    def update(self) -> None:
        """Move the watchman horizontally and update projectiles."""
        if self.moving_right:
            self.x += self.settings.ship_speed

        if self.moving_left:
            self.x -= self.settings.ship_speed

        max_x = self.boundaries.right - self.rect.width

        self.x = max(
            0.0,
            min(self.x, float(max_x)),
        )

        self.rect.x = int(self.x)
        self.arsenal.update_arsenal()

    def fire(self) -> bool:
        """Ask the arsenal to create a magic projectile."""
        return self.arsenal.fire_bullet()

    def draw(self) -> None:
        """Draw the watchman and all active projectiles."""
        self.screen.blit(
            self.image,
            self.rect,
        )

        self.arsenal.draw()

    def center_ship(self) -> None:
        """Center the watchman and stop horizontal movement."""
        self.rect.midbottom = self.boundaries.midbottom
        self.x = float(self.rect.x)
        self.moving_right = False
        self.moving_left = False