"""
Program: The Hollow Watch - Track 2
Author: Abass Hassan
Purpose: Loads and displays the custom Play button image.
Starter Code: Based on the Alien Invasion starter repository:
https://github.com/RedBeard41/alien_Invasion_starter.git
Asset: UI Pack RPG Expansion by Kenney, licensed under CC0.
Date: August 5, 2026
"""

from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class Button:
    """Create and display the custom Play button."""

    def __init__(
        self,
        ai_game: "AlienInvasion",
        msg: str,
    ) -> None:
        """Initialize the button image, font, position, and text."""
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.image = self._load_image()
        self.rect = self.image.get_rect()
        self.rect.center = self.screen.get_rect().center

        self.font = pygame.font.Font(
            str(self.settings.button_font_file),
            self.settings.button_font_size,
        )

        self._prep_msg(msg)

    def _load_image(self) -> pygame.Surface:
        """Load and resize the custom Play button image."""
        button_size = (
            self.settings.button_w,
            self.settings.button_h,
        )

        try:
            image = pygame.image.load(
                self.settings.play_button_file
            ).convert_alpha()

            return pygame.transform.scale(
                image,
                button_size,
            )

        except (FileNotFoundError, pygame.error):
            fallback_image = pygame.Surface(
                button_size,
                pygame.SRCALPHA,
            )

            fallback_image.fill(
                self.settings.button_color
            )

            return fallback_image

    def _prep_msg(self, msg: str) -> None:
        """Render and center the button text."""
        self.msg_image = self.font.render(
            msg,
            True,
            self.settings.text_color,
        )

        self.msg_image_rect = self.msg_image.get_rect(
            center=self.rect.center
        )

    def draw_button(self) -> None:
        """Draw the custom button image and its text."""
        self.screen.blit(
            self.image,
            self.rect,
        )

        self.screen.blit(
            self.msg_image,
            self.msg_image_rect,
        )

    def check_clicked(
        self,
        mouse_pos: tuple[int, int],
    ) -> bool:
        """Return True when the player clicks the button."""
        return self.rect.collidepoint(mouse_pos)
