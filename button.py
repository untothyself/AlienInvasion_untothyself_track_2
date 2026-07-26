"""
Program: The Hollow Watch - Track 2
Author: Abass Hassan
Purpose: Creates and displays the Play button.
Starter Code: Based on the Alien Invasion starter repository:
https://github.com/RedBeard41/alien_Invasion_starter.git
Date: July 26, 2026
"""
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class Button:
    """Create a centered game button."""

    def __init__(self, ai_game: 'AlienInvasion', msg: str) -> None:
        """Initialize the button's rectangle, font, and message."""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.font = pygame.font.Font(None, self.settings.button_font_size)
        self.rect = pygame.Rect(
            0, 0, self.settings.button_w, self.settings.button_h
        )
        self.rect.center = self.screen.get_rect().center
        self._prep_msg(msg)

    def _prep_msg(self, msg: str) -> None:
        """Render and center the button message."""
        self.msg_image = self.font.render(
            msg, True, self.settings.text_color, self.settings.button_color
        )
        self.msg_image_rect = self.msg_image.get_rect(center=self.rect.center)

    def draw_button(self) -> None:
        """Draw the button and its message."""
        self.screen.fill(self.settings.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def check_clicked(self, mouse_pos: tuple[int, int]) -> bool:
        """Return True when a click is inside the button."""
        return self.rect.collidepoint(mouse_pos)
