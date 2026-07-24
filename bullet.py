from typing import TYPE_CHECKING

import pygame
from pygame.sprite import Sprite

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class Bullet(Sprite):
    """Manage a bullet fired by the ship."""

    def __init__(self, ai_game: 'AlienInvasion') -> None:
        """Create a bullet at the ship's current position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.image = self._load_image()
        self.rect = self.image.get_rect()
        self.rect.midbottom = ai_game.ship.rect.midtop
        self.y: float = float(self.rect.y)

    def _load_image(self) -> pygame.Surface:
        """Load the bullet image or create a fallback rectangle."""
        size = (self.settings.bullet_width, self.settings.bullet_height)
        try:
            image = pygame.image.load(self.settings.bullet_file).convert_alpha()
            return pygame.transform.scale(image, size)
        except (FileNotFoundError, pygame.error):
            image = pygame.Surface(size, pygame.SRCALPHA)
            image.fill(self.settings.bullet_color)
            return image

    def update(self) -> None:
        """Move the bullet upward."""
        self.y -= self.settings.bullet_speed
        self.rect.y = int(self.y)

    def draw_bullet(self) -> None:
        """Draw the bullet."""
        self.screen.blit(self.image, self.rect)