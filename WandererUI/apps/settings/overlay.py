"""
Overlay widget.

Floats above the three-panel layout and provides the editing interface
for a single property.  The overlay displays the available options as a
navigable list and lets the user confirm or cancel a selection.

Two overlay modes exist:
  1. Property editing overlay — shows options for a specific property.
  2. Confirmation overlay — Apply/Discard staged changes on exit.
"""

from __future__ import annotations

from PyQt6.QtCore import QRectF, Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QPainter, QPainterPath, QKeyEvent
from PyQt6.QtWidgets import QWidget

from .models.state import SECTION_REGISTRY


class Overlay(QWidget):
    """
    Full-window overlay for editing a property value.

    Signals
    -------
    value_selected(section, property, value)
        Emitted when the user confirms a selection.
    overlay_closed()
        Emitted when the overlay is dismissed (Esc or confirm).
    """

    value_selected = pyqtSignal(str, str, str)
    overlay_closed = pyqtSignal()

    # Confirmation overlay signals
    apply_requested = pyqtSignal()
    discard_requested = pyqtSignal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._section = ""
        self._property = ""
        self._options: list[str] = []
        self._current_index = 0
        self._current_value = ""  # the value that is currently committed/effective
        self._mode = "property"  # "property" | "confirm"
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.hide()

    # ------------------------------------------------------------------ #
    # Public API — property editing
    # ------------------------------------------------------------------ #

    def open_for_property(
        self,
        section: str,
        prop: str,
        current_value: str,
    ) -> None:
        """Open the overlay to edit *prop* in *section*."""
        self._mode = "property"
        self._section = section
        self._property = prop
        self._current_value = current_value

        info = SECTION_REGISTRY.get(section)
        if info:
            for p in info.properties:
                if p.name == prop:
                    self._options = [o["name"] for o in p.options]
                    break
            else:
                self._options = []
        else:
            self._options = []

        # Pre-select the current value if it exists in the list.
        try:
            self._current_index = self._options.index(current_value)
        except ValueError:
            self._current_index = 0

        self.show()
        self.setFocus()
        self.update()

    # ------------------------------------------------------------------ #
    # Public API — confirmation overlay
    # ------------------------------------------------------------------ #

    def open_confirm_discard(self) -> None:
        """Open a confirmation overlay for Apply / Discard."""
        self._mode = "confirm"
        self._section = ""
        self._property = ""
        self._options = ["Apply Changes", "Discard Changes"]
        self._current_index = 0
        self.show()
        self.setFocus()
        self.update()

    # ------------------------------------------------------------------ #
    # Keyboard
    # ------------------------------------------------------------------ #

    def keyPressEvent(self, event: QKeyEvent) -> None:  # noqa: N802
        key = event.key()
        if key == Qt.Key.Key_Down:
            if self._current_index < len(self._options) - 1:
                self._current_index += 1
                # Live preview: emit value change on navigate in property mode
                if self._mode == "property":
                    self.value_selected.emit(
                        self._section,
                        self._property,
                        self._options[self._current_index],
                    )
                self.update()
        elif key == Qt.Key.Key_Up:
            if self._current_index > 0:
                self._current_index -= 1
                if self._mode == "property":
                    self.value_selected.emit(
                        self._section,
                        self._property,
                        self._options[self._current_index],
                    )
                self.update()
        elif key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self._confirm()
        elif key == Qt.Key.Key_Escape:
            self._cancel()
        else:
            super().keyPressEvent(event)

    # ------------------------------------------------------------------ #
    # Actions
    # ------------------------------------------------------------------ #

    def _confirm(self) -> None:
        if self._mode == "property":
            if self._options:
                self.value_selected.emit(
                    self._section,
                    self._property,
                    self._options[self._current_index],
                )
            self.hide()
            self.overlay_closed.emit()
        elif self._mode == "confirm":
            if self._current_index == 0:
                self.apply_requested.emit()
            else:
                self.discard_requested.emit()
            self.hide()
            self.overlay_closed.emit()

    def _cancel(self) -> None:
        if self._mode == "property":
            # Revert to the value before opening
            self.value_selected.emit(
                self._section,
                self._property,
                self._current_value,
            )
        self.hide()
        self.overlay_closed.emit()

    # ------------------------------------------------------------------ #
    # Painting
    # ------------------------------------------------------------------ #

    def paintEvent(self, _event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)

        w, h = self.width(), self.height()

        # Semi-transparent backdrop
        backdrop = QColor("#0a0b14")
        backdrop.setAlpha(180)
        painter.fillRect(0, 0, w, h, backdrop)

        # Overlay card
        card_w = min(420, w - 80)
        card_h = min(
            self._card_height(),
            h - 80,
        )
        cx = (w - card_w) / 2
        cy = (h - card_h) / 2

        # Card shadow
        shadow = QPainterPath()
        shadow.addRoundedRect(QRectF(cx + 2, cy + 2, card_w, card_h), 12, 12)
        shadow_c = QColor("#000000")
        shadow_c.setAlpha(80)
        painter.fillPath(shadow, shadow_c)

        # Card body
        card_path = QPainterPath()
        card_rect = QRectF(cx, cy, card_w, card_h)
        card_path.addRoundedRect(card_rect, 12, 12)
        painter.fillPath(card_path, QColor("#24283b"))

        # Card border
        from PyQt6.QtGui import QPen
        painter.setPen(QPen(QColor("#3b4261"), 1))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(card_rect, 12, 12)

        # Title
        title_font = QFont("Inter", 13)
        title_font.setWeight(QFont.Weight.Bold)
        painter.setFont(title_font)
        painter.setPen(QColor("#c0caf5"))
        title = self._property if self._mode == "property" else "Unsaved Changes"
        painter.drawText(
            QRectF(cx + 20, cy + 16, card_w - 40, 24),
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
            title,
        )

        # Subtitle
        if self._mode == "property":
            sub_font = QFont("Inter", 10)
            painter.setFont(sub_font)
            painter.setPen(QColor("#565f89"))
            painter.drawText(
                QRectF(cx + 20, cy + 42, card_w - 40, 18),
                Qt.AlignmentFlag.AlignLeft,
                f"Select {self._property.lower()} for {self._section}",
            )
        elif self._mode == "confirm":
            sub_font = QFont("Inter", 10)
            painter.setFont(sub_font)
            painter.setPen(QColor("#565f89"))
            painter.drawText(
                QRectF(cx + 20, cy + 42, card_w - 40, 18),
                Qt.AlignmentFlag.AlignLeft,
                "You have uncommitted changes",
            )

        # Divider
        painter.fillRect(QRectF(cx + 16, cy + 66, card_w - 32, 1), QColor("#3b4261"))

        # Options list
        item_h = 42
        list_y = cy + 76
        accent = QColor("#7aa2f7")
        text_primary = QColor("#c0caf5")
        text_muted = QColor("#a9b1d6")

        for i, option in enumerate(self._options):
            iy = list_y + i * (item_h + 2)
            if iy + item_h > cy + card_h - 10:
                break

            item_rect = QRectF(cx + 12, iy, card_w - 24, item_h)
            is_selected = i == self._current_index
            is_current = option == self._current_value and self._mode == "property"

            if is_selected:
                sel = QPainterPath()
                sel.addRoundedRect(item_rect, 6, 6)
                sel_color = QColor("#414868")
                painter.fillPath(sel, sel_color)

                # Left accent bar
                painter.fillRect(
                    QRectF(cx + 12, iy + 4, 3, item_h - 8), accent,
                )

            # Option text
            opt_font = QFont("Inter", 12)
            opt_font.setWeight(QFont.Weight.Medium if is_selected else QFont.Weight.Normal)
            painter.setFont(opt_font)
            painter.setPen(text_primary if is_selected else text_muted)
            painter.drawText(
                QRectF(cx + 28, iy, card_w - 80, item_h),
                Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
                option,
            )

            # Current value indicator (checkmark)
            if is_current:
                check_font = QFont("Inter", 14)
                check_font.setWeight(QFont.Weight.Bold)
                painter.setFont(check_font)
                painter.setPen(accent)
                painter.drawText(
                    QRectF(cx + card_w - 52, iy, 30, item_h),
                    Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignCenter,
                    "✓",
                )

            # Accent color swatch for accent options
            if self._property == "Accent" and self._mode == "property":
                from .models.state import SECTION_REGISTRY
                info = SECTION_REGISTRY.get(self._section)
                if info:
                    for p in info.properties:
                        if p.name == self._property:
                            for o in p.options:
                                if o["name"] == option and "value" in o:
                                    swatch_r = QRectF(cx + card_w - 72, iy + item_h / 2 - 7, 14, 14)
                                    sp = QPainterPath()
                                    sp.addRoundedRect(swatch_r, 3, 3)
                                    painter.fillPath(sp, QColor(o["value"]))
                                    break
                            break

        painter.end()

    def _card_height(self) -> float:
        """Calculate card height based on content."""
        header = 80  # title + subtitle + divider
        items = len(self._options) * 44
        padding = 20
        return header + items + padding
