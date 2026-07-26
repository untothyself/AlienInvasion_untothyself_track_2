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
        """Initialize the watchman and place him at the bottom center."""
        super().__init__()

        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.boundaries = self.screen.get_rect()
        self.arsenal = arsenal

        self.image = self._load_image()
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.boundaries.midbottom

        self.moving_right: bool = False
        self.moving_left: bool = False
        self.x: float = float(self.rect.x)

    def _load_image(self) -> pygame.Surface:
        """Load one watchman frame or create a fallback player shape."""
        size = (
            self.settings.ship_width,
            self.settings.ship_height,
        )

        try:
            sprite_sheet = pygame.image.load(
                self.settings.ship_file
            ).convert_alpha()

            # The watchman sheet contains three frames in one row.
            frame_count = 3
            frame_width = sprite_sheet.get_width() // frame_count
            frame_height = sprite_sheet.get_height()

            if frame_width <= 0 or frame_height <= 0:
                raise ValueError("The watchman sprite sheet has an invalid size.")

            first_frame = sprite_sheet.subsurface(
                pygame.Rect(
                    0,
                    0,
                    frame_width,
                    frame_height,
                )
            ).copy()

            return pygame.transform.scale(
                first_frame,
                size,
            )

        except (FileNotFoundError, pygame.error, ValueError):
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
        """Move the watchman and update his projectiles."""
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