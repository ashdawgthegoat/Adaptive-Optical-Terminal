# =============================================================================
# Settings Application — Status Bar
# =============================================================================
#
# Bottom bar displaying keyboard hints on the left and status text on the right.
# Thin SEPARATOR border on top edge.
#
# =============================================================================

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt

from .theme import Palette, FONT_FAMILY, FONT_SIZE


# =============================================================================
# StatusBar Widget
# =============================================================================

class StatusBar(QWidget):
    """Bottom bar showing keyboard hints and status information.

    Fixed height ~30px. Hints on left in SECONDARY, status on right in PRIMARY.
    """

    FIXED_HEIGHT = 30

    # =========================================================================
    # Construction
    # =========================================================================

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFixedHeight(self.FIXED_HEIGHT)
        self._build_ui()

    # =========================================================================
    # Public Interface
    # =========================================================================

    def set_hints(self, text: str) -> None:
        """Set the keyboard hint text shown on the left side.

        Args:
            text: Hint string describing available keyboard shortcuts.
        """
        self._hints_label.setText(text)

    def set_status(self, text: str) -> None:
        """Set the status text shown on the right side.

        Args:
            text: Status message to display.
        """
        self._status_label.setText(text)

    # =========================================================================
    # Internal — UI Construction
    # =========================================================================

    def _build_ui(self) -> None:
        """Build the horizontal layout with hints and status labels."""
        smaller_size = FONT_SIZE - 2

        self.setStyleSheet(
            f"border-top: 1px solid {Palette.SEPARATOR};"
            f" background-color: {Palette.BACKGROUND};"
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(0)

        # --- Hints (left) ---
        self._hints_label = QLabel("", self)
        self._hints_label.setStyleSheet(
            f"color: {Palette.SECONDARY};"
            f" font-family: '{FONT_FAMILY}';"
            f" font-size: {smaller_size}px;"
            f" border: none;"
        )
        self._hints_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        layout.addWidget(self._hints_label, 1)

        # --- Status (right) ---
        self._status_label = QLabel("", self)
        self._status_label.setStyleSheet(
            f"color: {Palette.PRIMARY};"
            f" font-family: '{FONT_FAMILY}';"
            f" font-size: {smaller_size}px;"
            f" border: none;"
        )
        self._status_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        layout.addWidget(self._status_label, 0)
