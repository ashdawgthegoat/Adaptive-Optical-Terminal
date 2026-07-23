"""
Placeholder preview for sections without a dedicated preview widget.

Shows a centred icon, section name, and a 'coming soon' subtitle.
"""

from __future__ import annotations

from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtGui import QColor, QFont, QPainter
from PyQt6.QtWidgets import QWidget


class PlaceholderPreview(QWidget):
    """Generic placeholder preview for unimplemented section previews."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._section_name = ""
        self._icon = "⚙"
        self.setMinimumSize(300, 300)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def set_section(self, name: str, icon: str) -> None:
        self._section_name = name
        self._icon = icon
        self.update()

    def paintEvent(self, _event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)

        w, h = self.width(), self.height()
        painter.fillRect(0, 0, w, h, QColor("#1a1b26"))

        # Centre point
        cx = w / 2
        cy = h / 2 - 20

        # Large icon
        icon_font = QFont("Segoe UI Emoji", 48)
        painter.setFont(icon_font)
        painter.setPen(QColor("#c0caf5"))
        painter.drawText(
            QRectF(0, cy - 40, w, 70),
            Qt.AlignmentFlag.AlignCenter,
            self._icon,
        )

        # Section name
        name_font = QFont("Inter", 18)
        name_font.setWeight(QFont.Weight.DemiBold)
        painter.setFont(name_font)
        painter.setPen(QColor("#c0caf5"))
        painter.drawText(
            QRectF(0, cy + 40, w, 30),
            Qt.AlignmentFlag.AlignCenter,
            self._section_name,
        )

        # Subtitle
        sub_font = QFont("Inter", 11)
        painter.setFont(sub_font)
        painter.setPen(QColor("#565f89"))
        painter.drawText(
            QRectF(0, cy + 72, w, 20),
            Qt.AlignmentFlag.AlignCenter,
            "Preview coming soon",
        )

        painter.end()
