# =============================================================================
# Settings Application — Option List Widget
# =============================================================================
#
# Keyboard-navigable vertical list of text items. Core reusable widget.
# Supports selection highlighting, active item markers, and scroll-into-view.
#
# =============================================================================

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QLabel, QFrame,
)
from PyQt6.QtCore import Qt, pyqtSignal

from ..theme import Palette, FONT_FAMILY, FONT_SIZE


# =============================================================================
# OptionList Widget
# =============================================================================

class OptionList(QWidget):
    """A keyboard-navigable vertical list of text items.

    Displays a flat list of string labels. One item is "selected"
    (highlighted with ACCENT left border). Items can be marked "active"
    (shown with a ● prefix in ACCENT color).
    """

    # =========================================================================
    # Signals
    # =========================================================================

    item_activated = pyqtSignal(str)
    """Emitted when Enter is pressed on the selected item."""

    selection_changed = pyqtSignal(int)
    """Emitted when the selection moves to a new index."""

    # =========================================================================
    # Construction
    # =========================================================================

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self._items: list[str] = []
        self._active_item: str | None = None
        self._selected_index: int = -1
        self._labels: list[QLabel] = []

        self._build_ui()

    # =========================================================================
    # Public Interface
    # =========================================================================

    def set_items(
        self, items: list[str], active_item: str | None = None
    ) -> None:
        """Populate the list with items.

        Args:
            items: List of string labels to display.
            active_item: The currently active/applied item name, or None.
        """
        self._items = list(items)
        self._active_item = active_item

        # Clear existing labels
        self._clear_labels()

        # Create new labels
        for text in self._items:
            label = self._make_item_label(text)
            self._content_layout.addWidget(label)
            self._labels.append(label)

        # Select first item if available
        if self._items:
            self._selected_index = 0
        else:
            self._selected_index = -1

        self._update_styles()

    def selected_item(self) -> str | None:
        """Return the currently selected item text, or None."""
        if 0 <= self._selected_index < len(self._items):
            return self._items[self._selected_index]
        return None

    def selected_index(self) -> int:
        """Return the current selection index."""
        return self._selected_index

    def item_count(self) -> int:
        """Return the number of items in the list."""
        return len(self._items)

    def move_up(self) -> None:
        """Move selection up by one."""
        if self._selected_index > 0:
            self._selected_index -= 1
            self._update_styles()
            self._ensure_visible()
            self.selection_changed.emit(self._selected_index)

    def move_down(self) -> None:
        """Move selection down by one."""
        if self._selected_index < len(self._items) - 1:
            self._selected_index += 1
            self._update_styles()
            self._ensure_visible()
            self.selection_changed.emit(self._selected_index)

    def move_to_start(self) -> None:
        """Select the first item."""
        if self._items and self._selected_index != 0:
            self._selected_index = 0
            self._update_styles()
            self._ensure_visible()
            self.selection_changed.emit(self._selected_index)

    def move_to_end(self) -> None:
        """Select the last item."""
        last = len(self._items) - 1
        if self._items and self._selected_index != last:
            self._selected_index = last
            self._update_styles()
            self._ensure_visible()
            self.selection_changed.emit(self._selected_index)

    def set_selected_index(self, index: int) -> None:
        """Programmatically set the selected index.

        Args:
            index: The index to select.
        """
        if 0 <= index < len(self._items):
            self._selected_index = index
            self._update_styles()
            self._ensure_visible()

    # =========================================================================
    # Keyboard Handling
    # =========================================================================

    def keyPressEvent(self, event) -> None:
        """Handle keyboard navigation within the list."""
        key = event.key()

        if key in (Qt.Key.Key_Up, Qt.Key.Key_K):
            self.move_up()
        elif key in (Qt.Key.Key_Down, Qt.Key.Key_J):
            self.move_down()
        elif key == Qt.Key.Key_Home:
            self.move_to_start()
        elif key == Qt.Key.Key_End:
            self.move_to_end()
        elif key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            item = self.selected_item()
            if item is not None:
                self.item_activated.emit(item)
        else:
            super().keyPressEvent(event)

    # =========================================================================
    # Internal — UI Construction
    # =========================================================================

    def _build_ui(self) -> None:
        """Build the scroll area and content layout."""
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)

        # --- Scroll area ---
        self._scroll = QScrollArea(self)
        self._scroll.setWidgetResizable(True)
        self._scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self._scroll.setFrameShape(QFrame.Shape.NoFrame)

        # --- Content container ---
        self._content = QWidget()
        self._content_layout = QVBoxLayout(self._content)
        self._content_layout.setContentsMargins(0, 4, 0, 4)
        self._content_layout.setSpacing(0)
        self._content_layout.addStretch()

        self._scroll.setWidget(self._content)
        outer_layout.addWidget(self._scroll)

    def _make_item_label(self, text: str) -> QLabel:
        """Create a QLabel for an item row."""
        label = QLabel(self._content)
        label.setFont(label.font())
        label.setMinimumHeight(28)
        label.setContentsMargins(0, 0, 0, 0)
        return label

    # =========================================================================
    # Internal — Style Updates
    # =========================================================================

    def _update_styles(self) -> None:
        """Update all label text and styles based on selection and active state."""
        for i, label in enumerate(self._labels):
            text = self._items[i]
            is_active = text == self._active_item
            is_selected = i == self._selected_index

            # Build prefix
            prefix = f"<span style='color:{Palette.ACCENT};'>● </span>" if is_active else "  "

            # Build label text
            label.setText(f"{prefix}{text}")
            label.setTextFormat(Qt.TextFormat.RichText)

            # Build style
            if is_selected:
                label.setStyleSheet(
                    f"background-color: {Palette.SURFACE_SELECTED};"
                    f" border-left: 3px solid {Palette.ACCENT};"
                    f" color: {Palette.PRIMARY};"
                    f" font-family: '{FONT_FAMILY}';"
                    f" font-size: {FONT_SIZE}px;"
                    f" padding: 4px 8px;"
                )
            else:
                label.setStyleSheet(
                    f"background-color: transparent;"
                    f" border-left: 3px solid transparent;"
                    f" color: {Palette.PRIMARY};"
                    f" font-family: '{FONT_FAMILY}';"
                    f" font-size: {FONT_SIZE}px;"
                    f" padding: 4px 8px;"
                )

    def _clear_labels(self) -> None:
        """Remove all item labels from the layout."""
        for label in self._labels:
            self._content_layout.removeWidget(label)
            label.deleteLater()
        self._labels.clear()

    def _ensure_visible(self) -> None:
        """Scroll so the selected item is visible."""
        if 0 <= self._selected_index < len(self._labels):
            label = self._labels[self._selected_index]
            self._scroll.ensureWidgetVisible(label, 0, 30)
