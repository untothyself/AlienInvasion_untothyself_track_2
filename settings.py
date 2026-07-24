from pathlib import Path


class Settings:
    """Store all static and changing settings for Alien Invasion."""

    def __init__(self) -> None:
        """Initialize the game's settings and asset paths."""
        # Screen settings
        self.name: str = "Alien Invasion"
        self.screen_width: int = 1200
        self.screen_height: int = 800
        self.FPS: int = 60
        self.bg_color: tuple[int, int, int] = (10, 15, 35)

        # Project and asset folders
        self.base_dir: Path = Path(__file__).resolve().parent
        self.assets_dir: Path = self._find_existing_dir(["Assets", "assets"])

        self.bg_file: str = self._resolve_asset_path(
            "images", ["Starbasesnow.png", "starbases_now.png", "starbasesnow.png"]
        )

        # Ship settings
        self.ship_file: str = self._resolve_asset_path(
            "images", ["ship.png", "ship2.png", "ship2(no bg).png", "ship_to_nob.png"]
        )
        self.ship_width: int = 60
        self.ship_height: int = 40
        self.ship_color: tuple[int, int, int] = (80, 180, 255)
        self.starting_ship_count: int = 3

        # Bullet settings
        self.bullet_file: str = self._resolve_asset_path(
            "images", ["laserBlast.png", "laser_blast.png", "beams.png"]
        )
        self.bullet_width: int = 10
        self.bullet_height: int = 30
        self.bullet_amount: int = 5
        self.bullet_color: tuple[int, int, int] = (255, 230, 80)

        # Alien settings
        self.alien_file: str = self._resolve_asset_path("images", ["enemy_4.png"])
        self.alien_w: int = 40
        self.alien_h: int = 40
        self.alien_color: tuple[int, int, int] = (100, 230, 120)
        self.fleet_drop_speed: int = 10

        # Sound settings
        self.laser_sound: str = self._resolve_asset_path(
            "sound", ["laser.mp3", "laser.wav"]
        )
        self.impact_sound: str = self._resolve_asset_path(
            "sound", ["impactSound.mp3", "impactSound.wav"]
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

        # Persistent score file
        self.score_file: Path = self.assets_dir / "file" / "scores.json"

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

    def _resolve_asset_path(self, subfolder: str, candidates: list[str]) -> str:
        """Return the first existing asset path, or the expected first path."""
        folder = self.assets_dir / subfolder
        for name in candidates:
            candidate = folder / name
            if candidate.is_file():
                return str(candidate)
        return str(folder / candidates[0])
        
