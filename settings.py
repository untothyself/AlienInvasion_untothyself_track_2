"""
Program: The Hollow Watch - Track 2
Author: Abass Hassan
Purpose: Stores game settings and handles paths for images, sounds, and data.
Starter Code: Based on the Alien Invasion starter repository:
https://github.com/RedBeard41/alien_Invasion_starter.git
Date: July 26, 2026
"""
from pathlib import Path


class Settings:
    """Store all static and changing settings for The Hollow Watch."""

    def __init__(self) -> None:
        """Initialize the game's settings and asset paths."""
        # Screen settings
        self.name: str = "The Hollow Watch - Track 2"
        self.screen_width: int = 1200
        self.screen_height: int = 800
        self.FPS: int = 60
        self.bg_color: tuple[int, int, int] = (10, 15, 35)

        # Project and asset folders
        self.base_dir: Path = Path(__file__).resolve().parent
        self.assets_dir: Path = self._find_existing_dir(
            ["Assets", "assets"]
        )

        # Background assets
        self.bg_file: str = self._resolve_asset_path(
            "images",
            ["gothic_background.png"],
        )

        self.middleground_file: str = self._resolve_asset_path(
            "images",
            ["gothic_town.png"],
        )

        # Ship settings
        self.ship_file: str = self._resolve_asset_path(
            "images",
            ["watchman.png"],
        )       

        self.ship_width: int = 52
        self.ship_height: int = 70
        self.ship_color: tuple[int, int, int] = (80, 180, 255)
        self.starting_ship_count: int = 3

        # Bullet settings
        self.bullet_file: str = self._resolve_asset_path(
            "images",
            ["light_bolt.png"],
        )

        self.bullet_width: int = 10
        self.bullet_height: int = 24
        self.bullet_amount: int = 5
        self.bullet_color: tuple[int, int, int] = (255, 230, 80)

        # Alien settings
        self.alien_file: str = self._resolve_asset_path(
            "images",
            ["hollow_townsman.png"],
        )

        self.alien_w: int = 48
        self.alien_h: int = 60
        self.alien_color: tuple[int, int, int] = (100, 230, 120)
        self.fleet_drop_speed: int = 10

        # Sound settings
        self.laser_sound: str = self._resolve_asset_path(
            "sound",
            ["laser.mp3", "laser.wav"],
        )

        self.impact_sound: str = self._resolve_asset_path(
            "sound",
            ["impactSound.mp3", "impactSound.wav"],
        )

        # Difficulty settings
        self.difficulty_scale: float = 1.05

        # Button and HUD settings
        self.button_w: int = 200
        self.button_h: int = 50
        self.button_color: tuple[int, int, int] = (0, 135, 0)
        self.text_color: tuple[int, int, int] = (255, 255, 255)
        self.button_font_size: int = 48
        self.HUD_font_size: int = 20

        # Custom font paths
        self.font_dir: Path = (
            self.assets_dir / "Fonts" / "Silkscreen"
        )

        self.hud_font_file: Path = (
            self.font_dir / "Silkscreen-Regular.ttf"
        )

        self.button_font_file: Path = (
            self.font_dir / "Silkscreen-Bold.ttf"
        )

        # Persistent score file
        self.score_file: Path = (
            self.assets_dir / "file" / "scores.json"
        )

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self) -> None:
        """Reset settings that change as the player clears levels."""
        self.ship_speed: float = 5.0
        self.bullet_speed: float = 7.0
        self.alien_speed: float = 2.0
        self.fleet_direction: int = 1

    def increase_difficulty(self) -> None:
        """Increase movement speeds when a level is cleared."""
        self.ship_speed *= self.difficulty_scale
        self.bullet_speed *= self.difficulty_scale
        self.alien_speed *= self.difficulty_scale

    def _find_existing_dir(self, candidates: list[str]) -> Path:
        """Return the first existing asset directory."""
        for name in candidates:
            path = self.base_dir / name

            if path.is_dir():
                return path

        return self.base_dir / candidates[0]

    def _resolve_asset_path(
        self,
        subfolder: str,
        candidates: list[str],
    ) -> str:
        """Return the first existing asset path or its expected path."""
        folder = self.assets_dir / subfolder

        for name in candidates:
            candidate = folder / name

            if candidate.is_file():
                return str(candidate)

        return str(folder / candidates[0])
