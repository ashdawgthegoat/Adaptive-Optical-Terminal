"""
Properties panel (right panel).

Displays the editable properties for the currently selected section.
Each property shows its name and current effective value; staged values
are marked with a small accent-coloured dot.
"""

from __future__ import annotations

from PyQt6.QtCore import QRectF, Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QPainter, QPainterPath, QKeyEvent
from PyQt6.QtWidgets import QWidget

from .models.state import SECTION_REGISTRY
from .models.staged_settings import StagedSettings


class PropertiesPanel(QWidget):
    """Right-hand property list with keyboard navigation."""

    # (section_name, property_name)
    property_activated = pyqtSignal(str, str)
    back_requested = pyqtSignal()
    # Emitted when the selection highlight moves.
    property_changed = pyqtSignal(str, str)

    ITEM_HEIGHT = 48
    ITEM_GAP = 4
    HEADER_HEIGHT = 52

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._section_name = ""
        self._properties: list[str] = []
        self._current_index = 0
        self._focus_active = False
        self._staged_settings: StagedSettings | None = None
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setMinimumWidth(200)

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #

    def set_staged_settings(self, staged: StagedSettings) -> None:
        self._staged_settings = staged

    def set_section(self, section_name: str) -> None:
        self._section_name = section_name
        info = SECTION_REGISTRY.get(section_name)
        self._properties = [p.name for p in info.properties] if info else []
        self._current_index = 0
        self.update()

    def refresh(self) -> None:
        self.update()

    def set_focus_active(self, active: bool) -> None:
        self._focus_active = active
        self.update()

    def get_current_property(self) -> str:
        if 0 <= self._current_index < len(self._properties):
            return self._properties[self._current_index]
        return ""

    # ------------------------------------------------------------------ #
    # Keyboard
    # ------------------------------------------------------------------ #

    def keyPressEvent(self, event: QKeyEvent) -> None:  # noqa: N802
        key = event.key()
        if key == Qt.Key.Key_Down:
            if self._current_index < len(self._properties) - 1:
                self._current_index += 1
                self.property_changed.emit(self._section_name, self.get_current_property())
                self.update()
        elif key == Qt.Key.Key_Up:
            if self._current_index > 0:
                self._current_index -= 1
                self.property_changed.emit(self._section_name, self.get_current_property())
                self.update()
        elif key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            if self._properties:
                self.property_activated.emit(
                    self._section_name, self.get_current_property(),
                )
        elif key == Qt.Key.Key_Escape:
            self.back_requested.emit()
        else:
            super().keyPressEvent(event)

    # ------------------------------------------------------------------ #
    # Painting
    # ------------------------------------------------------------------ #

    def paintEvent(self, _event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)

        w, h = self.width(), self.height()

        # Panel background
        painter.fillRect(0, 0, w, h, QColor("#24283b"))

        # Header: section name in accent colour
        header_font = QFont("Inter", 10)
        header_font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 2.0)
        header_font.setWeight(QFont.Weight.Bold)
        painter.setFont(header_font)
        painter.setPen(QColor("#7aa2f7"))
        painter.drawText(
            QRectF(20, 0, w - 24, self.HEADER_HEIGHT),
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
            self._section_name.upper(),
        )

        accent = QColor("#7aa2f7")
        dimmed = QColor("#414868")
        text_primary = QColor("#c0caf5")
        text_muted = QColor("#565f89")

        y = float(self.HEADER_HEIGHT)
        for i, prop_name in enumerate(self._properties):
            item_rect = QRectF(8, y, w - 16, self.ITEM_HEIGHT)
            is_selected = i == self._current_index

            if is_selected:
                sel_path = QPainterPath()
                sel_path.addRoundedRect(item_rect, 6, 6)
                painter.fillPath(sel_path, QColor("#414868"))

                bar_color = accent if self._focus_active else dimmed
                painter.fillRect(QRectF(8, y + 4, 3, self.ITEM_HEIGHT - 8), bar_color)

            # Property name
            name_font = QFont("Inter", 12)
            name_font.setWeight(QFont.Weight.Medium if is_selected else QFont.Weight.Normal)
            painter.setFont(name_font)
            painter.setPen(text_primary if is_selected else QColor("#a9b1d6"))
            painter.drawText(
                QRectF(22, y, w * 0.5, self.ITEM_HEIGHT),
                Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
                prop_name,
            )

            # Current effective value
            value = ""
            is_staged = False
            if self._staged_settings and self._section_name:
                value = self._staged_settings.get_effective(self._section_name, prop_name)
                is_staged = self._staged_settings.is_staged(self._section_name, prop_name)

            # Staged indicator dot
            if is_staged:
                painter.setPen(Qt.PenStyle.NoPen)
                painter.setBrush(accent)
                dot_x = w - 24
                dot_y = y + self.ITEM_HEIGHT / 2
                painter.drawEllipse(QRectF(dot_x - 3, dot_y - 3, 6, 6))

            # Value text (right-aligned)
            value_font = QFont("Inter", 11)
            painter.setFont(value_font)
            painter.setPen(text_muted)
            right_margin = 34 if is_staged else 20
            painter.drawText(
                QRectF(w * 0.4, y, w * 0.6 - right_margin, self.ITEM_HEIGHT),
                Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight,
                value,
            )

            y += self.ITEM_HEIGHT + self.ITEM_GAP

        painter.end()
