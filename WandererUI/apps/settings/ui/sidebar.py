# =============================================================================
# Settings Application — Sidebar
# =============================================================================
#
# Left sidebar showing setting category labels. Keyboard-navigable.
# Category switches instantly on arrow key movement (no Enter required).
#
# =============================================================================

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt, pyqtSignal

from .theme import Palette, FONT_FAMILY, FONT_SIZE


# =============================================================================
# Sidebar Widget
# =============================================================================

class Sidebar(QWidget):
    """Left sidebar listing setting categories.

    Fixed width 200px. Selected category has ACCENT left border and
    SURFACE_SELECTED background. Navigation is instant — no Enter required.
    """

    FIXED_WIDTH = 200

    # =========================================================================
    # Signals
    # =========================================================================

    category_changed = pyqtSignal(int)
    """Emitted when the selected category changes. Carries the new index."""

    # =========================================================================
    # Construction
    # =========================================================================

    def __init__(
        self, categories: list[str], parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setFixedWidth(self.FIXED_WIDTH)

        self._categories = list(categories)
        self._selected_index = 0
        self._labels: list[QLabel] = []

        self._build_ui()
        self._update_styles()

    # =========================================================================
    # Public Interface
    # =========================================================================

    def selected_index(self) -> int:
        """Return the currently selected category index."""
        return self._selected_index

    def move_up(self) -> None:
        """Move selection up by one and emit category_changed."""
        if self._selected_index > 0:
            self._selected_index -= 1
            self._update_styles()
            self.category_changed.emit(self._selected_index)

    def move_down(self) -> None:
        """Move selection down by one and emit category_changed."""
        if self._selected_index < len(self._categories) - 1:
            self._selected_index += 1
            self._update_styles()
            self.category_changed.emit(self._selected_index)

    def set_selected_index(self, index: int) -> None:
        """Programmatically set the selected category.

        Args:
            index: Category index to select.
        """
        if 0 <= index < len(self._categories):
            self._selected_index = index
            self._update_styles()

    # =========================================================================
    # Keyboard Handling
    # =========================================================================

    def keyPressEvent(self, event) -> None:
        """Handle keyboard navigation in the sidebar."""
        key = event.key()

        if key in (Qt.Key.Key_Up, Qt.Key.Key_K):
            self.move_up()
        elif key in (Qt.Key.Key_Down, Qt.Key.Key_J):
            self.move_down()
        elif key == Qt.Key.Key_Home:
            if self._selected_index != 0:
                self._selected_index = 0
                self._update_styles()
                self.category_changed.emit(self._selected_index)
        elif key == Qt.Key.Key_End:
            last = len(self._categories) - 1
            if self._selected_index != last:
                self._selected_index = last
                self._update_styles()
                self.category_changed.emit(self._selected_index)
        elif key == Qt.Key.Key_Q:
            window = self.window()
            if window is not None:
                window.close()
        else:
            super().keyPressEvent(event)

    # =========================================================================
    # Internal — UI Construction
    # =========================================================================

    def _build_ui(self) -> None:
        """Build the sidebar layout with header, category labels, and separator."""
        self.setStyleSheet(f"background-color: {Palette.BACKGROUND};")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 12, 0, 12)
        layout.setSpacing(0)

        # --- Header ---
        header = QLabel("SETTINGS", self)
        header.setStyleSheet(
            f"color: {Palette.SECONDARY};"
            f" font-family: '{FONT_FAMILY}';"
            f" font-size: {FONT_SIZE - 2}px;"
            f" padding: 8px 16px 12px 16px;"
            f" background-color: transparent;"
        )
        layout.addWidget(header)

        # --- Category labels ---
        for text in self._categories:
            label = QLabel(text, self)
            label.setMinimumHeight(32)
            self._labels.append(label)
            layout.addWidget(label)

        layout.addStretch()

        # --- Right-edge separator line ---
        separator = QFrame(self)
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setStyleSheet(
            f"color: {Palette.SEPARATOR};"
            f" background-color: {Palette.SEPARATOR};"
            f" max-width: 1px;"
        )
        separator.setFixedWidth(1)

        # Place separator on the right edge using a parent-level trick:
        # We'll use the layout margin approach instead
        # Actually, we handle this via the settings_window layout

    # =========================================================================
    # Internal — Style Updates
    # =========================================================================

    def _update_styles(self) -> None:
        """Update all category label styles based on selection."""
        for i, label in enumerate(self._labels):
            if i == self._selected_index:
                label.setStyleSheet(
                    f"color: {Palette.PRIMARY};"
                    f" font-family: '{FONT_FAMILY}';"
                    f" font-size: {FONT_SIZE}px;"
                    f" background-color: {Palette.SURFACE_SELECTED};"
                    f" border-left: 3px solid {Palette.ACCENT};"
                    f" padding: 6px 16px 6px 13px;"
                )
            else:
                label.setStyleSheet(
                    f"color: {Palette.SECONDARY};"
                    f" font-family: '{FONT_FAMILY}';"
                    f" font-size: {FONT_SIZE}px;"
                    f" background-color: transparent;"
                    f" border-left: 3px solid transparent;"
                    f" padding: 6px 16px 6px 13px;"
                )
