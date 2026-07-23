"""
Navigation panel (left panel).

Displays the list of settings sections and handles keyboard navigation.
Custom-painted for a polished appearance.
"""

from __future__ import annotations

from PyQt6.QtCore import QRectF, Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QPainter, QPainterPath, QKeyEvent
from PyQt6.QtWidgets import QWidget

from .models.state import SECTIONS, SECTION_REGISTRY


class NavigationPanel(QWidget):
    """Left-hand section list with keyboard navigation."""

    # Emitted when the selection highlight moves (for preview updates).
    section_changed = pyqtSignal(str)
    # Emitted when Enter is pressed to drill into a section.
    section_activated = pyqtSignal(str)

    ITEM_HEIGHT = 48
    ITEM_GAP = 4
    HEADER_HEIGHT = 52

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._sections = SECTIONS
        self._current_index = 0
        self._focus_active = True  # visual emphasis when this panel owns focus
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setMinimumWidth(200)

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #

    def get_current_section(self) -> str:
        return self._sections[self._current_index]

    def set_focus_active(self, active: bool) -> None:
        self._focus_active = active
        self.update()

    # ------------------------------------------------------------------ #
    # Keyboard
    # ------------------------------------------------------------------ #

    def keyPressEvent(self, event: QKeyEvent) -> None:  # noqa: N802
        key = event.key()
        if key == Qt.Key.Key_Down:
            if self._current_index < len(self._sections) - 1:
                self._current_index += 1
                self.section_changed.emit(self.get_current_section())
                self.update()
        elif key == Qt.Key.Key_Up:
            if self._current_index > 0:
                self._current_index -= 1
                self.section_changed.emit(self.get_current_section())
                self.update()
        elif key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.section_activated.emit(self.get_current_section())
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

        # Header
        header_font = QFont("Inter", 10)
        header_font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 3.0)
        header_font.setWeight(QFont.Weight.Bold)
        painter.setFont(header_font)
        painter.setPen(QColor("#565f89"))
        painter.drawText(
            QRectF(20, 0, w - 24, self.HEADER_HEIGHT),
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
            "SETTINGS",
        )

        # Section items
        accent = QColor("#7aa2f7")
        dimmed_accent = QColor("#414868")
        text_primary = QColor("#c0caf5")
        text_muted = QColor("#565f89")

        y = float(self.HEADER_HEIGHT)
        for i, section_name in enumerate(self._sections):
            info = SECTION_REGISTRY[section_name]
            item_rect = QRectF(8, y, w - 16, self.ITEM_HEIGHT)

            is_selected = i == self._current_index

            if is_selected:
                # Selected background
                sel_path = QPainterPath()
                sel_path.addRoundedRect(item_rect, 6, 6)
                painter.fillPath(sel_path, QColor("#414868"))

                # Left accent bar
                bar_color = accent if self._focus_active else dimmed_accent
                painter.fillRect(QRectF(8, y + 4, 3, self.ITEM_HEIGHT - 8), bar_color)

            # Icon
            icon_font = QFont("Segoe UI Emoji", 16)
            painter.setFont(icon_font)
            painter.setPen(text_primary if is_selected else text_muted)
            painter.drawText(
                QRectF(22, y, 36, self.ITEM_HEIGHT),
                Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignCenter,
                info.icon,
            )

            # Section name
            name_font = QFont("Inter", 12)
            name_font.setWeight(QFont.Weight.Medium if is_selected else QFont.Weight.Normal)
            painter.setFont(name_font)
            painter.setPen(text_primary if is_selected else QColor("#a9b1d6"))
            painter.drawText(
                QRectF(58, y, w - 70, self.ITEM_HEIGHT),
                Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
                section_name,
            )

            y += self.ITEM_HEIGHT + self.ITEM_GAP

        painter.end()
