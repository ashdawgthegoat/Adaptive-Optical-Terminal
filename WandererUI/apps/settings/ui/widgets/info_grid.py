# =============================================================================
# Settings Application — Info Grid Widget
# =============================================================================
#
# Displays key-value pairs in a two-column grid layout.
# Purely informational — no interactive elements.
#
# =============================================================================

from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt6.QtCore import Qt

from ..theme import Palette, FONT_FAMILY, FONT_SIZE


# =============================================================================
# InfoGrid Widget
# =============================================================================

class InfoGrid(QWidget):
    """Two-column grid displaying key-value information pairs.

    Keys are rendered in SECONDARY color on the left.
    Values are rendered in PRIMARY color on the right.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self._layout = QGridLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setHorizontalSpacing(24)
        self._layout.setVerticalSpacing(8)
        self._layout.setColumnStretch(1, 1)

        self._labels: list[tuple[QLabel, QLabel]] = []

    # =========================================================================
    # Public Interface
    # =========================================================================

    def set_info(self, data: dict[str, str]) -> None:
        """Replace all displayed info with the given key-value pairs.

        Args:
            data: Dictionary of label-value pairs to display.
        """
        self.clear()

        for row, (key, value) in enumerate(data.items()):
            key_label = self._make_key_label(key)
            value_label = self._make_value_label(value)

            self._layout.addWidget(key_label, row, 0, Qt.AlignmentFlag.AlignTop)
            self._layout.addWidget(value_label, row, 1, Qt.AlignmentFlag.AlignTop)

            self._labels.append((key_label, value_label))

    def clear(self) -> None:
        """Remove all displayed info."""
        for key_label, value_label in self._labels:
            self._layout.removeWidget(key_label)
            key_label.deleteLater()
            self._layout.removeWidget(value_label)
            value_label.deleteLater()

        self._labels.clear()

    # =========================================================================
    # Internal Helpers
    # =========================================================================

    def _make_key_label(self, text: str) -> QLabel:
        """Create a styled key label."""
        label = QLabel(text, self)
        label.setStyleSheet(
            f"color: {Palette.SECONDARY};"
            f" font-family: '{FONT_FAMILY}';"
            f" font-size: {FONT_SIZE}px;"
        )
        label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        return label

    def _make_value_label(self, text: str) -> QLabel:
        """Create a styled value label."""
        label = QLabel(text, self)
        label.setStyleSheet(
            f"color: {Palette.PRIMARY};"
            f" font-family: '{FONT_FAMILY}';"
            f" font-size: {FONT_SIZE}px;"
        )
        label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        return label
