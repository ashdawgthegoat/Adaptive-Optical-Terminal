# =============================================================================
# Settings Application — Base Page
# =============================================================================
#
# Common interface for all settings pages. Provides default implementations
# for lifecycle hooks and hint text. Not abstract — subclasses override
# as needed.
#
# =============================================================================

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt


# =============================================================================
# BasePage Widget
# =============================================================================

class BasePage(QWidget):
    """Base class for all settings pages.

    Provides a common interface for page title, keyboard hints, and
    lifecycle hooks (on_enter / on_leave). Subclasses override as needed.
    """

    # =========================================================================
    # Construction
    # =========================================================================

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    # =========================================================================
    # Public Interface
    # =========================================================================

    def page_title(self) -> str:
        """Return the page title. Override in subclasses."""
        return ""

    def hint_text(self) -> str:
        """Return keyboard hint string for the StatusBar.

        Override in subclasses for page-specific hints.
        """
        return "↑↓ Navigate   Enter Select   Esc Back"

    def on_enter(self) -> None:
        """Called when the page becomes the active page.

        Override in subclasses to refresh data or set initial focus.
        """
        pass

    def on_leave(self) -> None:
        """Called when the page is no longer the active page.

        Override in subclasses to clean up or save state.
        """
        pass
