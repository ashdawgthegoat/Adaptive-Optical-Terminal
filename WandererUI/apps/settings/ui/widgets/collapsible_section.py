# =============================================================================
# Settings Application — Collapsible Section Widget
# =============================================================================
#
# A section with a header that toggles between expanded and collapsed states.
# No animation — instant show/hide for retro terminal aesthetic.
#
# =============================================================================

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import pyqtSignal

from ..theme import Palette, FONT_FAMILY, FONT_SIZE


# =============================================================================
# CollapsibleSection Widget
# =============================================================================

class CollapsibleSection(QWidget):
    """A titled section that can be expanded or collapsed.

    Header shows ▼ when expanded and ▶ when collapsed.
    Content widget is shown/hidden instantly — no animation.
    """

    # =========================================================================
    # Signals
    # =========================================================================

    toggled = pyqtSignal(bool)
    """Emitted when the section is expanded or collapsed. True = expanded."""

    # =========================================================================
    # Construction
    # =========================================================================

    def __init__(self, title: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self._title = title.upper()
        self._expanded = True
        self._content: QWidget | None = None

        self._build_ui()

    # =========================================================================
    # Public Interface
    # =========================================================================

    def set_content(self, widget: QWidget) -> None:
        """Set the child content widget to show/hide.

        Args:
            widget: The widget to display inside this section.
        """
        if self._content is not None:
            self._layout.removeWidget(self._content)
            self._content.deleteLater()

        self._content = widget
        self._layout.addWidget(self._content)
        self._content.setVisible(self._expanded)

    def is_expanded(self) -> bool:
        """Return True if the section is currently expanded."""
        return self._expanded

    def expand(self) -> None:
        """Expand the section, showing the content widget."""
        if not self._expanded:
            self._expanded = True
            self._update_header()
            if self._content is not None:
                self._content.setVisible(True)
            self.toggled.emit(True)

    def collapse(self) -> None:
        """Collapse the section, hiding the content widget."""
        if self._expanded:
            self._expanded = False
            self._update_header()
            if self._content is not None:
                self._content.setVisible(False)
            self.toggled.emit(False)

    def toggle(self) -> None:
        """Toggle between expanded and collapsed."""
        if self._expanded:
            self.collapse()
        else:
            self.expand()

    @property
    def title(self) -> str:
        """The section title text (uppercase)."""
        return self._title

    # =========================================================================
    # Internal — UI Construction
    # =========================================================================

    def _build_ui(self) -> None:
        """Build the header label and layout."""
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

        # --- Header label ---
        self._header = QLabel(self)
        self._header.setStyleSheet(
            f"color: {Palette.SECONDARY};"
            f" font-family: '{FONT_FAMILY}';"
            f" font-size: {FONT_SIZE}px;"
            f" padding: 8px 4px;"
            f" border-bottom: 1px solid {Palette.SEPARATOR};"
            f" background-color: transparent;"
        )
        self._layout.addWidget(self._header)

        self._update_header()

    def _update_header(self) -> None:
        """Update the header label text based on expansion state."""
        indicator = "▼" if self._expanded else "▶"
        self._header.setText(f"{indicator}  {self._title}")
