from typing import TYPE_CHECKING

import pygame
from pygame.sprite import Sprite

from arsenal import Arsenal

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class Ship(Sprite):
    """Manage the player's ship."""

    def __init__(self, ai_game: 'AlienInvasion', arsenal: Arsenal) -> None:
        """Initialize the ship and place it at the bottom center."""
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
        """Load the ship image or create a simple fallback ship."""
        size = (self.settings.ship_width, self.settings.ship_height)
        try:
            image = pygame.image.load(self.settings.ship_file).convert_alpha()
            return pygame.transform.scale(image, size)
        except (FileNotFoundError, pygame.error):
            image = pygame.Surface(size, pygame.SRCALPHA)
            points = [(size[0] // 2, 0), (0, size[1]), (size[0], size[1])]
            pygame.draw.polygon(image, self.settings.ship_color, points)
            return image

    def update(self) -> None:
        """Move the ship and update its bullets."""
        if self.moving_right:
            self.x += self.settings.ship_speed
        if self.moving_left:
            self.x -= self.settings.ship_speed

        max_x = self.boundaries.right - self.rect.width
        self.x = max(0.0, min(self.x, float(max_x)))
        self.rect.x = int(self.x)
        self.arsenal.update_arsenal()

    def fire(self) -> bool:
        """Ask the arsenal to create a bullet."""
        return self.arsenal.fire_bullet()

    def draw(self) -> None:
        """Draw the ship and all active bullets."""
        self.screen.blit(self.image, self.rect)
        self.arsenal.draw()

    def center_ship(self) -> None:
        """Center the ship and stop its movement."""
        self.rect.midbottom = self.boundaries.midbottom
        self.x = float(self.rect.x)
        self.moving_right = False
        self.moving_left = False