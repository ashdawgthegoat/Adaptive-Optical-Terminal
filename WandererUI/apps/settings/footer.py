"""
Footer bar.

Displays context-sensitive keyboard navigation hints with pill-badge
key indicators.
"""

from __future__ import annotations

from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtGui import QColor, QFont, QPainter, QPainterPath
from PyQt6.QtWidgets import QWidget


# Context → list of (key_label, action_text) pairs.
_HINTS: dict[str, list[tuple[str, str]]] = {
    "sections": [
        ("↑↓", "Navigate"),
        ("⏎", "Select"),
        ("Esc", "Quit"),
    ],
    "properties": [
        ("↑↓", "Navigate"),
        ("⏎", "Edit"),
        ("Esc", "Back"),
    ],
    "overlay": [
        ("↑↓", "Navigate"),
        ("⏎", "Confirm"),
        ("Esc", "Cancel"),
    ],
}


class Footer(QWidget):
    """Slim footer showing context-sensitive navigation key hints."""

    FOOTER_HEIGHT = 36

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._context = "sections"
        self.setFixedHeight(self.FOOTER_HEIGHT)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def set_context(self, context: str) -> None:
        if context in _HINTS:
            self._context = context
            self.update()

    # ------------------------------------------------------------------ #
    # Painting
    # ------------------------------------------------------------------ #

    def paintEvent(self, _event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)

        w, h = self.width(), self.height()

        # Background
        painter.fillRect(0, 0, w, h, QColor("#1a1b26"))

        # Top border
        painter.fillRect(QRectF(0, 0, w, 1), QColor("#3b4261"))

        hints = _HINTS.get(self._context, _HINTS["sections"])

        key_font = QFont("Inter", 10)
        key_font.setWeight(QFont.Weight.Bold)
        action_font = QFont("Inter", 10)

        badge_bg = QColor("#3b4261")
        key_text_color = QColor("#c0caf5")
        action_text_color = QColor("#565f89")

        # Measure total width for centering
        painter.setFont(key_font)
        kfm = painter.fontMetrics()
        painter.setFont(action_font)
        afm = painter.fontMetrics()

        total_w = 0.0
        spacing = 24.0
        badge_pad_h = 12  # horizontal padding inside badge
        badge_pad_v = 4
        items_widths: list[tuple[float, float]] = []
        for key_label, action_text in hints:
            kw = kfm.horizontalAdvance(key_label) + badge_pad_h * 2
            aw = afm.horizontalAdvance(action_text)
            items_widths.append((kw, aw))
            total_w += kw + 6 + aw

        total_w += spacing * (len(hints) - 1)
        x_cursor = (w - total_w) / 2

        badge_h = h - 14

        for idx, (key_label, action_text) in enumerate(hints):
            kw, aw = items_widths[idx]

            # Key badge
            badge_rect = QRectF(x_cursor, (h - badge_h) / 2, kw, badge_h)
            bp = QPainterPath()
            bp.addRoundedRect(badge_rect, 4, 4)
            painter.fillPath(bp, badge_bg)

            painter.setFont(key_font)
            painter.setPen(key_text_color)
            painter.drawText(badge_rect, Qt.AlignmentFlag.AlignCenter, key_label)

            x_cursor += kw + 6

            # Action text
            painter.setFont(action_font)
            painter.setPen(action_text_color)
            painter.drawText(
                QRectF(x_cursor, 0, aw, h),
                Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
                action_text,
            )

            x_cursor += aw + spacing

        painter.end()
