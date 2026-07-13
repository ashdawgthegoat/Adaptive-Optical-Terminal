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
from services.maaya import Maaya
from apps.settings.application import (
    create_settings_application
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

    # --- Create presentation services ---
    maaya = Maaya()

    # --- Create window ---

    window = create_settings_application(
        maaya
    )

    # --- show window ---
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
