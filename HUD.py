"""
Program: The Hollow Watch - Track 2
Author: Abass Hassan
Purpose: Displays the score, high score, maximum score, and remaining lives.
Starter Code: Based on the Alien Invasion starter repository:
https://github.com/RedBeard41/alien_Invasion_starter.git
Date: July 26, 2026
"""
import json
from pathlib import Path
from typing import TYPE_CHECKING

import pygame.font

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class HUD:
    """Display scores and remaining lives on the game screen."""

    def __init__(self, ai_game: 'AlienInvasion') -> None:
        """Initialize scorekeeping and text-rendering attributes."""
        self.screen = ai_game.screen
        self.stats = ai_game.stats
        self.settings = ai_game.settings
        self.font = pygame.font.Font(None, self.settings.HUD_font_size)
        self.score_file: Path = self.settings.score_file

        self._load_high_score()
        self.update_scores()

    def _load_high_score(self) -> None:
        """Load the saved high score, or use zero when it cannot be read."""
        try:
            if not self.score_file.is_file() or self.score_file.stat().st_size == 0:
                self.stats.high_score = 0
                return

            with self.score_file.open("r", encoding="utf-8") as file:
                data = json.load(file)

            saved_score = data.get("high_score", 0)
            self.stats.high_score = saved_score if isinstance(saved_score, int) else 0
        except (json.JSONDecodeError, OSError, TypeError):
            self.stats.high_score = 0

    def _save_high_score(self) -> None:
        """Save the high score without crashing the game if writing fails."""
        try:
            self.score_file.parent.mkdir(parents=True, exist_ok=True)
            with self.score_file.open("w", encoding="utf-8") as file:
                json.dump({"high_score": self.stats.high_score}, file)
        except OSError:
            # The game can continue even when the score file is not writable.
            pass

    def update_scores(self) -> None:
        """Render the current score, run maximum, high score, and lives."""
        self.score_image = self.font.render(
            f"Score: {self.stats.score}", True, self.settings.text_color
        )
        self.score_rect = self.score_image.get_rect(topleft=(10, 10))

        self.max_score_image = self.font.render(
            f"Max: {self.stats.max_score}", True, (255, 255, 0)
        )
        self.max_score_rect = self.max_score_image.get_rect(topleft=(10, 35))

        self.high_score_image = self.font.render(
            f"High: {self.stats.high_score}", True, (0, 255, 255)
        )
        self.high_score_rect = self.high_score_image.get_rect(topleft=(10, 60))

        self.lives_image = self.font.render(
            f"Ships: {self.stats.ships_left}", True, self.settings.text_color
        )
        self.lives_rect = self.lives_image.get_rect(topleft=(10, 85))

    def draw_scores(self) -> None:
        """Draw all HUD information."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.max_score_image, self.max_score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.draw_lives()

    def draw_lives(self) -> None:
        """Draw the number of ships remaining."""
        self.screen.blit(self.lives_image, self.lives_rect)

    def check_high_score(self) -> None:
        """Save a new high score when the current score is higher."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self._save_high_score()
            self.update_scores()