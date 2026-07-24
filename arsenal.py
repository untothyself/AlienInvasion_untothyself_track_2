from typing import TYPE_CHECKING

import pygame

from bullet import Bullet

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class Arsenal:
    """Manage all bullets fired by the ship."""

    def __init__(self, ai_game: 'AlienInvasion') -> None:
        self.ai_game = ai_game
        self.settings = ai_game.settings
        self.bullets = pygame.sprite.Group()

    def update_arsenal(self) -> None:
        """Move bullets and remove bullets that leave the screen."""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                bullet.kill()

    def fire_bullet(self) -> bool:
        """Create a bullet when the on-screen limit allows it."""
        if len(self.bullets) >= self.settings.bullet_amount:
            return False

        self.bullets.add(Bullet(self.ai_game))
        return True

    def draw(self) -> None:
        """Draw all active bullets."""
        self.bullets.draw(self.ai_game.screen)