"""
Program: The Hollow Watch - Track 2
Author: Abass Hassan
Purpose: Represents and moves one magic light-bolt projectile.
Starter Code: Based on the Alien Invasion starter repository:
https://github.com/RedBeard41/alien_Invasion_starter.git
Date: July 26, 2026
Projectile Asset: Light bolt from Pixel Art Spells by DevWizard.
Asset Source: https://opengameart.org/content/pixel-art-spells
License: Creative Commons Zero, CC0.
Asset File: Assets/images/light_bolt.png
"""
from typing import TYPE_CHECKING

import pygame
from pygame.sprite import Sprite

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class Bullet(Sprite):
    """Represent one magic light bolt fired by the watchman."""

    def __init__(self, ai_game: "AlienInvasion") -> None:
        """Create a light bolt above the watchman's current position."""
        super().__init__()

        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.image = self._load_image()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        # Place the projectile directly above the player.
        self.rect.midbottom = ai_game.ship.rect.midtop

        # Store the vertical position as a decimal for smooth movement.
        self.y: float = float(self.rect.y)

    def _load_image(self) -> pygame.Surface:
        """Load the light-bolt image or create a fallback projectile."""
        size = (
            self.settings.bullet_width,
            self.settings.bullet_height,
        )

        try:
            image = pygame.image.load(
                self.settings.bullet_file
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

            fallback_image.fill(
                self.settings.bullet_color
            )

            return fallback_image

    def update(self) -> None:
        """Move the light bolt upward across the screen."""
        self.y -= self.settings.bullet_speed
        self.rect.y = int(self.y)

    def draw_bullet(self) -> None:
        """Draw the light bolt at its current position."""
        self.screen.blit(
            self.image,
            self.rect,
        )