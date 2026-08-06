"""
Program: The Hollow Watch - Track 2
Author: Abass Hassan
Purpose: Displays a custom Gothic HUD with score, high score, and lives.
Starter Code: Based on the Alien Invasion starter repository:
https://github.com/RedBeard41/alien_Invasion_starter.git
Date: August 5, 2026
"""

import json
from pathlib import Path
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class HUD:
    """Display scores and remaining lives in a custom Gothic panel."""

    def __init__(self, ai_game: "AlienInvasion") -> None:
        """Initialize the HUD panel, fonts, and score information."""
        self.screen = ai_game.screen
        self.stats = ai_game.stats
        self.settings = ai_game.settings
        self.score_file: Path = self.settings.score_file

        self.font = pygame.font.Font(
            str(self.settings.hud_font_file),
            self.settings.HUD_font_size,
        )

        self.title_font = pygame.font.Font(
            str(self.settings.button_font_file),
            22,
        )

        self.panel_rect = pygame.Rect(
            15,
            15,
            330,
            165,
        )

        self.panel_surface = pygame.Surface(
            self.panel_rect.size,
            pygame.SRCALPHA,
        )

        self._prepare_panel()
        self._load_high_score()
        self.update_scores()

    def _prepare_panel(self) -> None:
        """Create the transparent Gothic HUD background and border."""
        self.panel_surface.fill(
            (15, 10, 25, 215)
        )

        pygame.draw.rect(
            self.panel_surface,
            (175, 135, 75),
            self.panel_surface.get_rect(),
            width=4,
            border_radius=10,
        )

        pygame.draw.rect(
            self.panel_surface,
            (80, 55, 95),
            self.panel_surface.get_rect().inflate(-12, -12),
            width=2,
            border_radius=7,
        )

    def _load_high_score(self) -> None:
        """Load the saved high score or use zero if reading fails."""
        try:
            if (
                not self.score_file.is_file()
                or self.score_file.stat().st_size == 0
            ):
                self.stats.high_score = 0
                return

            with self.score_file.open(
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)

            saved_score = data.get("high_score", 0)

            if isinstance(saved_score, int):
                self.stats.high_score = saved_score
            else:
                self.stats.high_score = 0

        except (
            json.JSONDecodeError,
            OSError,
            TypeError,
        ):
            self.stats.high_score = 0

    def _save_high_score(self) -> None:
        """Save the high score without interrupting the game."""
        try:
            self.score_file.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            with self.score_file.open(
                "w",
                encoding="utf-8",
            ) as file:
                json.dump(
                    {"high_score": self.stats.high_score},
                    file,
                )

        except OSError:
            pass

    def update_scores(self) -> None:
        """Render the title, score, high score, maximum, and lives."""
        left = self.panel_rect.left + 25

        self.title_image = self.title_font.render(
            "THE HOLLOW WATCH",
            True,
            (235, 205, 145),
        )

        self.title_rect = self.title_image.get_rect(
            topleft=(left, self.panel_rect.top + 18)
        )

        self.score_image = self.font.render(
            f"Score: {self.stats.score}",
            True,
            (245, 245, 245),
        )

        self.score_rect = self.score_image.get_rect(
            topleft=(left, self.panel_rect.top + 58)
        )

        self.high_score_image = self.font.render(
            f"High Score: {self.stats.high_score}",
            True,
            (120, 220, 255),
        )

        self.high_score_rect = self.high_score_image.get_rect(
            topleft=(left, self.panel_rect.top + 84)
        )

        self.max_score_image = self.font.render(
            f"Run Maximum: {self.stats.max_score}",
            True,
            (255, 220, 110),
        )

        self.max_score_rect = self.max_score_image.get_rect(
            topleft=(left, self.panel_rect.top + 110)
        )

        self.lives_image = self.font.render(
            f"Lives: {self.stats.ships_left}",
            True,
            (255, 155, 155),
        )

        self.lives_rect = self.lives_image.get_rect(
            topleft=(left, self.panel_rect.top + 136)
        )

    def draw_scores(self) -> None:
        """Draw the custom HUD panel and all game information."""
        self.screen.blit(
            self.panel_surface,
            self.panel_rect,
        )

        self.screen.blit(
            self.title_image,
            self.title_rect,
        )

        self.screen.blit(
            self.score_image,
            self.score_rect,
        )

        self.screen.blit(
            self.high_score_image,
            self.high_score_rect,
        )

        self.screen.blit(
            self.max_score_image,
            self.max_score_rect,
        )

        self.screen.blit(
            self.lives_image,
            self.lives_rect,
        )

    def check_high_score(self) -> None:
        """Save and display a new high score when one is earned."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self._save_high_score()
            self.update_scores()