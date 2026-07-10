# =============================================================================
# Settings Application — Modules Page (Placeholder)
# =============================================================================
#
# Stub page — feature not yet implemented.
#
# =============================================================================

import sys
from pathlib import Path

from PyQt6.QtWidgets import QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

from .base_page import BasePage
from ..theme import Palette, FONT_FAMILY, FONT_SIZE


# =============================================================================
# ModulesPage
# =============================================================================

class ModulesPage(BasePage):
    """Placeholder page for Modules settings."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._build_ui()

    # =========================================================================
    # BasePage Overrides
    # =========================================================================

    def page_title(self) -> str:
        return "Modules"

    def hint_text(self) -> str:
        return "Esc Back"

    # =========================================================================
    # Internal — UI Construction
    # =========================================================================

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel("NOT YET AVAILABLE", self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(
            f"color: {Palette.SECONDARY};"
            f" font-family: '{FONT_FAMILY}';"
            f" font-size: {FONT_SIZE}px;"
        )
        layout.addWidget(label)


# =============================================================================
# Standalone Entry Point
# =============================================================================

if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[4]
    sys.path.insert(0, str(project_root))

    from PyQt6.QtWidgets import QApplication
    from apps.settings.ui.theme import load_font, build_stylesheet

    assets = project_root / "assets"

    app = QApplication(sys.argv)
    load_font(str(assets / "fonts" / "system" / "DepartureMonoNerdFont-Regular.otf"))
    app.setStyleSheet(build_stylesheet())

    page = ModulesPage()
    page.setMinimumSize(600, 400)
    page.show()
    sys.exit(app.exec())
