# =============================================================================
# Settings Application — About Page
# =============================================================================
#
# Displays system information via InfoGrid: hostname, platform, CPU,
# memory, storage, and battery status. Refreshed on page entry.
#
# =============================================================================

import sys
from pathlib import Path

from PyQt6.QtWidgets import QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

from .base_page import BasePage
from ..theme import Palette, FONT_FAMILY, FONT_SIZE
from ..widgets.info_grid import InfoGrid


# =============================================================================
# AboutPage
# =============================================================================

class AboutPage(BasePage):
    """Displays system information in a two-column grid.

    Shows hostname, platform, CPU usage, memory usage, storage usage,
    and battery status from the SystemInfoProvider.
    """

    # =========================================================================
    # Construction
    # =========================================================================

    def __init__(self, system_info_provider, parent=None) -> None:
        super().__init__(parent)
        self._provider = system_info_provider
        self._build_ui()

    # =========================================================================
    # BasePage Overrides
    # =========================================================================

    def page_title(self) -> str:
        return "About"

    def hint_text(self) -> str:
        return "Esc Back"

    def on_enter(self) -> None:
        """Refresh system info from the provider."""
        self._refresh()

    # =========================================================================
    # Internal — UI Construction
    # =========================================================================

    def _build_ui(self) -> None:
        """Build the page layout with header and info grid."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # --- Header ---
        header = QLabel("ABOUT", self)
        header.setStyleSheet(
            f"color: {Palette.PRIMARY};"
            f" font-family: '{FONT_FAMILY}';"
            f" font-size: {FONT_SIZE + 4}px;"
        )
        header.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(header)

        # --- Info grid ---
        self._info_grid = InfoGrid(self)
        layout.addWidget(self._info_grid)

        layout.addStretch()

    # =========================================================================
    # Internal — Data Refresh
    # =========================================================================

    def _refresh(self) -> None:
        """Query the provider and update the info grid."""
        p = self._provider

        data = {
            "Hostname": p.hostname(),
            "Platform": p.platform_name(),
            "CPU Usage": p.cpu_usage(),
            "Memory": p.memory_usage(),
            "Storage": p.storage_usage(),
            "Battery": p.battery_status(),
        }

        self._info_grid.set_info(data)


# =============================================================================
# Standalone Entry Point
# =============================================================================

if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[4]
    sys.path.insert(0, str(project_root))

    from PyQt6.QtWidgets import QApplication
    from apps.settings.ui.theme import load_font, build_stylesheet
    from apps.settings.providers import SystemInfoProvider

    assets = project_root / "assets"

    app = QApplication(sys.argv)
    load_font(str(assets / "fonts" / "system" / "DepartureMonoNerdFont-Regular.otf"))
    app.setStyleSheet(build_stylesheet())

    page = AboutPage(SystemInfoProvider())
    page.on_enter()
    page.setMinimumSize(600, 400)
    page.show()
    sys.exit(app.exec())
