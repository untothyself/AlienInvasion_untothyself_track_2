from typing import TYPE_CHECKING

import pygame
from pygame.sprite import Sprite

if TYPE_CHECKING:
    from alien_fleet import AlienFleet

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, fleet: 'AlienFleet', x: float, y: float) -> None:
        """Initialize the alien at the fleet-calculated position."""
        super().__init__()
        self.fleet = fleet
        self.settings = fleet.settings
        self.screen = fleet.game.screen
        self.boundaries = self.screen.get_rect()

        self.image = self._load_image()
        self.rect = self.image.get_rect()
        self.x: float = x
        self.y: float = y
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def _load_image(self) -> pygame.Surface:
        """Load the alien image or create a fallback alien shape."""
        size = (self.settings.alien_w, self.settings.alien_h)
        try:
            image = pygame.image.load(self.settings.alien_file).convert_alpha()
            return pygame.transform.scale(image, size)
        except (FileNotFoundError, pygame.error):
            image = pygame.Surface(size, pygame.SRCALPHA)
            pygame.draw.ellipse(image, self.settings.alien_color, image.get_rect())
            return image

    def check_edges(self) -> bool:
        """Return True when the alien reaches either horizontal edge."""
        return self.rect.right >= self.boundaries.right or self.rect.left <= 0

    def update(self) -> None:
        """Move the alien horizontally with the fleet."""
        self.x += self.settings.alien_speed * self.fleet.fleet_direction
        self.rect.x = int(self.x)

    def draw_alien(self) -> None:
        """Draw the alien."""
        self.screen.blit(self.image, self.rect)
