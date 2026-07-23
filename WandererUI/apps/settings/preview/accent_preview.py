"""
Accent colour preview widget.

Renders a miniature desktop with the selected accent colour prominently
featured on title bars, selection indicators, buttons, and a colour
swatch strip to show the accent at various opacities.
"""

from __future__ import annotations

from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtGui import QColor, QFont, QPainter, QPainterPath
from PyQt6.QtWidgets import QWidget


ACCENT_COLORS: dict[str, str] = {
    "Blue": "#7aa2f7",
    "Purple": "#bb9af7",
    "Cyan": "#7dcfff",
    "Green": "#9ece6a",
    "Orange": "#e0af68",
    "Pink": "#ff007c",
    "Red": "#f7768e",
    "Teal": "#73daca",
}


class AccentPreview(QWidget):
    """Renders a recoloured miniature desktop featuring the accent colour."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._accent_name = "Blue"
        self.setMinimumSize(300, 300)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def set_accent(self, accent_name: str) -> None:
        if accent_name in ACCENT_COLORS:
            self._accent_name = accent_name
            self.update()

    # ------------------------------------------------------------------ #
    # Painting
    # ------------------------------------------------------------------ #

    def paintEvent(self, _event) -> None:  # noqa: N802
        accent = QColor(ACCENT_COLORS.get(self._accent_name, "#7aa2f7"))
        bg = QColor("#1a1b26")
        surface = QColor("#24283b")
        text_col = QColor("#c0caf5")
        muted = QColor("#565f89")

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        painter.fillRect(0, 0, w, h, bg)

        pad = 24
        dw = w - pad * 2
        dh = h - pad * 2 - 55  # room for swatch strip + label
        dx, dy = float(pad), float(pad)

        # Frame
        frame = QPainterPath()
        frame.addRoundedRect(QRectF(dx - 3, dy - 3, dw + 6, dh + 6), 10, 10)
        painter.fillPath(frame, QColor("#3b4261"))

        # Desktop area
        desktop = QRectF(dx, dy, dw, dh)
        dp = QPainterPath()
        dp.addRoundedRect(desktop, 7, 7)
        painter.setClipPath(dp)
        painter.fillRect(desktop, bg)

        # ---- Accent title bar ---- #
        tb_h = dh * 0.08
        painter.fillRect(QRectF(dx, dy, dw, tb_h), accent)

        # Title bar text
        font = QFont("Inter", max(7, int(tb_h * 0.42)))
        font.setWeight(QFont.Weight.Bold)
        painter.setFont(font)
        painter.setPen(QColor("#1a1b26"))
        painter.drawText(
            QRectF(dx + 12, dy, dw - 24, tb_h),
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
            "Settings",
        )

        # Window dots (dark on accent)
        dot_r = tb_h * 0.16
        dot_y = dy + tb_h / 2
        for i in range(3):
            cx = dx + dw - 12 - i * (dot_r * 2 + 5)
            c = QColor("#1a1b26")
            c.setAlpha(120)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(c)
            painter.drawEllipse(QRectF(cx - dot_r, dot_y - dot_r, dot_r * 2, dot_r * 2))

        # ---- Sidebar ---- #
        sb_w = dw * 0.25
        sb_rect = QRectF(dx, dy + tb_h, sb_w, dh - tb_h - dh * 0.07)
        painter.fillRect(sb_rect, surface)

        # Sidebar items with accent selected
        item_h = sb_rect.height() / 6
        for i in range(5):
            iy = sb_rect.y() + 6 + i * item_h
            item_rect = QRectF(dx + 6, iy, sb_w - 12, item_h - 4)
            if i == 0:
                # Selected: accent background
                sel = QPainterPath()
                sel.addRoundedRect(item_rect, 4, 4)
                ac = QColor(accent)
                ac.setAlpha(50)
                painter.fillPath(sel, ac)
                painter.fillRect(QRectF(dx + 6, iy, 3, item_h - 4), accent)

            line_col = QColor(text_col if i == 0 else muted)
            line_col.setAlpha(180 if i == 0 else 100)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(line_col)
            lw = sb_w * (0.55 + (i % 3) * 0.08)
            painter.drawRoundedRect(
                QRectF(dx + 18, iy + item_h * 0.35, lw - 26, 3), 1.5, 1.5,
            )

        # ---- Content area ---- #
        cx_start = dx + sb_w + 1
        content_w = dw - sb_w - 1
        content_y = dy + tb_h
        content_h = dh - tb_h - dh * 0.07

        painter.fillRect(QRectF(cx_start, content_y, content_w, content_h), bg)

        # Accent-coloured buttons/elements
        btn_w = content_w * 0.35
        btn_h = content_h * 0.07
        btn_y = content_y + 14

        # Primary button
        btn_rect = QRectF(cx_start + 14, btn_y, btn_w, btn_h)
        btn_path = QPainterPath()
        btn_path.addRoundedRect(btn_rect, 4, 4)
        painter.fillPath(btn_path, accent)
        painter.setPen(QColor("#1a1b26"))
        painter.setFont(QFont("Inter", max(6, int(btn_h * 0.45))))
        painter.drawText(btn_rect, Qt.AlignmentFlag.AlignCenter, "Apply")

        # Secondary button (outline)
        btn2_rect = QRectF(cx_start + 14 + btn_w + 8, btn_y, btn_w, btn_h)
        from PyQt6.QtGui import QPen
        painter.setPen(QPen(accent, 1.5))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(btn2_rect, 4, 4)
        painter.setPen(accent)
        painter.drawText(btn2_rect, Qt.AlignmentFlag.AlignCenter, "Cancel")

        # Content cards
        card_y = btn_y + btn_h + 14
        card_h = content_h * 0.16
        for i in range(3):
            cy = card_y + i * (card_h + 8)
            if cy + card_h > content_y + content_h:
                break
            card = QRectF(cx_start + 14, cy, content_w - 28, card_h)
            cp = QPainterPath()
            cp.addRoundedRect(card, 5, 5)
            painter.fillPath(cp, surface)

            # Accent dot
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(accent)
            painter.drawEllipse(QRectF(card.x() + 10, card.y() + card_h / 2 - 3, 6, 6))

            # Lines
            line_c = QColor(text_col)
            line_c.setAlpha(100)
            painter.setBrush(line_c)
            painter.drawRoundedRect(
                QRectF(card.x() + 24, card.y() + card_h * 0.35, content_w * 0.4, 3),
                1.5, 1.5,
            )
            line_c2 = QColor(text_col)
            line_c2.setAlpha(60)
            painter.setBrush(line_c2)
            painter.drawRoundedRect(
                QRectF(card.x() + 24, card.y() + card_h * 0.6, content_w * 0.25, 2.5),
                1.2, 1.2,
            )

        # ---- Taskbar ---- #
        taskbar_h = dh * 0.07
        taskbar_rect = QRectF(dx, dy + dh - taskbar_h, dw, taskbar_h)
        painter.fillRect(taskbar_rect, surface)

        # Active indicator on taskbar
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(accent)
        painter.drawRoundedRect(
            QRectF(dx + dw / 2 - 12, taskbar_rect.y() + taskbar_h - 3, 24, 3),
            1.5, 1.5,
        )

        painter.setClipping(False)

        # ---- Swatch strip ---- #
        swatch_y = dy + dh + 12
        swatch_h = 18
        swatch_w = dw / 8
        painter.setFont(QFont("Inter", 8))
        opacities = [255, 200, 160, 120, 80, 50, 30, 15]
        for i, alpha in enumerate(opacities):
            sx = dx + i * swatch_w
            c = QColor(accent)
            c.setAlpha(alpha)
            rect = QRectF(sx + 2, swatch_y, swatch_w - 4, swatch_h)
            sp = QPainterPath()
            sp.addRoundedRect(rect, 3, 3)
            painter.fillPath(sp, c)

        # Label
        painter.setPen(QColor("#565f89"))
        painter.setFont(QFont("Inter", 10))
        painter.drawText(
            QRectF(0, h - 22, w, 20),
            Qt.AlignmentFlag.AlignCenter,
            f"Accent: {self._accent_name}",
        )

        painter.end()
