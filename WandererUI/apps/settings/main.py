# =============================================================================
# Settings Application — Entry Point
# =============================================================================
#
# Launch the Settings application. Can be run as:
#   python -m apps.settings.main     (from WandererUI/)
#   python apps/settings/main.py     (from WandererUI/)
#
# =============================================================================

import sys
from pathlib import Path

# Ensure project root is in path
project_root = Path(__file__).resolve().parents[2]  # WandererUI/
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QApplication

from apps.settings.ui.theme import load_font, build_stylesheet
from apps.settings.ui.settings_window import SettingsWindow
from apps.settings.controller import SettingsController
from apps.settings.providers import (
    ThemeProvider,
    WallpaperProvider,
    FontProvider,
    SystemInfoProvider,
)


# =============================================================================
# Main
# =============================================================================

def main() -> None:
    """Create and launch the Settings application."""
    app = QApplication(sys.argv)

    # --- Paths ---
    assets = project_root / "assets"
    font_path = assets / "fonts" / "system" / "DepartureMonoNerdFont-Regular.otf"

    # --- Load font and stylesheet ---
    load_font(str(font_path))
    app.setStyleSheet(build_stylesheet())

    # --- Create providers ---
    providers = {
        "theme": ThemeProvider(str(assets / "themes")),
        "wallpaper": WallpaperProvider(str(assets / "wallpapers")),
        "font": FontProvider(str(assets / "fonts")),
        "system_info": SystemInfoProvider(),
    }

    # --- Create controller ---
    controller = SettingsController()

    # --- Create and show window ---
    window = SettingsWindow(controller, providers)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
