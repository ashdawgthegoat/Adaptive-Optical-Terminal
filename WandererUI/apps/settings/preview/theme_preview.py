"""
Miniature desktop preview for theme selection.

Paints a scaled-down desktop environment (title bar, sidebar, content area,
taskbar) using the colour palette of the currently selected theme.
"""

from __future__ import annotations

import math

from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtGui import QColor, QPainter, QPainterPath, QPen, QFont
from PyQt6.QtWidgets import QWidget


# ------------------------------------------------------------------ #
# Theme palettes
# ------------------------------------------------------------------ #

THEME_PALETTES: dict[str, dict[str, str]] = {
    "Tokyo Night":     {"bg": "#1a1b26", "surface": "#24283b", "accent": "#7aa2f7", "text": "#c0caf5", "surface2": "#414868"},
    "Catppuccin Mocha": {"bg": "#1e1e2e", "surface": "#313244", "accent": "#cba6f7", "text": "#cdd6f4", "surface2": "#45475a"},
    "Nord":            {"bg": "#2e3440", "surface": "#3b4252", "accent": "#88c0d0", "text": "#eceff4", "surface2": "#434c5e"},
    "Gruvbox Dark":    {"bg": "#282828", "surface": "#3c3836", "accent": "#fe8019", "text": "#ebdbb2", "surface2": "#504945"},
    "Rosé Pine":       {"bg": "#191724", "surface": "#26233a", "accent": "#ebbcba", "text": "#e0def4", "surface2": "#403d52"},
    "Dracula":         {"bg": "#282a36", "surface": "#44475a", "accent": "#bd93f9", "text": "#f8f8f2", "surface2": "#6272a4"},
    "One Dark":        {"bg": "#282c34", "surface": "#3e4451", "accent": "#61afef", "text": "#abb2bf", "surface2": "#4b5263"},
    "Solarized Dark":  {"bg": "#002b36", "surface": "#073642", "accent": "#268bd2", "text": "#839496", "surface2": "#586e75"},
}


class ThemePreview(QWidget):
    """Renders a miniature desktop coloured with the active theme palette."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._theme = "Tokyo Night"
        self.setMinimumSize(300, 300)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #

    def set_theme(self, theme_name: str) -> None:
        if theme_name in THEME_PALETTES:
            self._theme = theme_name
            self.update()

    # ------------------------------------------------------------------ #
    # Painting
    # ------------------------------------------------------------------ #

    def paintEvent(self, _event) -> None:  # noqa: N802
        p = THEME_PALETTES.get(self._theme, THEME_PALETTES["Tokyo Night"])
        bg = QColor(p["bg"])
        surface = QColor(p["surface"])
        surface2 = QColor(p["surface2"])
        accent = QColor(p["accent"])
        text = QColor(p["text"])

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()

        # Fill entire widget background
        painter.fillRect(0, 0, w, h, QColor("#1a1b26"))

        # Desktop area (centered with padding)
        pad = 24
        dw = w - pad * 2
        dh = h - pad * 2
        dx, dy = float(pad), float(pad)

        # Monitor frame
        frame_path = QPainterPath()
        frame_path.addRoundedRect(QRectF(dx - 4, dy - 4, dw + 8, dh + 8), 12, 12)
        painter.fillPath(frame_path, QColor("#3b4261"))

        # Desktop background
        desktop = QRectF(dx, dy, dw, dh)
        dp = QPainterPath()
        dp.addRoundedRect(desktop, 8, 8)
        painter.setClipPath(dp)
        painter.fillRect(desktop, bg)

        # ---- Title bar ---- #
        tb_h = dh * 0.07
        tb_rect = QRectF(dx, dy, dw, tb_h)
        painter.fillRect(tb_rect, surface)

        # Window dots
        dot_r = tb_h * 0.18
        dot_y = dy + tb_h / 2
        colors = ["#f7768e", "#e0af68", "#9ece6a"]
        for i, c in enumerate(colors):
            cx = dx + 12 + i * (dot_r * 2 + 5)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(c))
            painter.drawEllipse(QRectF(cx - dot_r, dot_y - dot_r, dot_r * 2, dot_r * 2))

        # Title text
        font = QFont("Inter", max(7, int(tb_h * 0.42)))
        painter.setFont(font)
        text_muted = QColor(text)
        text_muted.setAlpha(160)
        painter.setPen(text_muted)
        painter.drawText(
            QRectF(dx + 60, dy, dw - 70, tb_h),
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft,
            "File  Edit  View  Help",
        )

        # ---- Sidebar ---- #
        sb_w = dw * 0.22
        sb_rect = QRectF(dx, dy + tb_h, sb_w, dh - tb_h - dh * 0.06)
        painter.fillRect(sb_rect, surface)

        # Sidebar items
        item_h = (sb_rect.height()) / 7
        for i in range(6):
            iy = sb_rect.y() + 6 + i * item_h
            item_rect = QRectF(dx + 6, iy, sb_w - 12, item_h - 4)
            if i == 0:
                # Selected item
                sel_path = QPainterPath()
                sel_path.addRoundedRect(item_rect, 4, 4)
                painter.fillPath(sel_path, surface2)
                # Accent indicator
                painter.fillRect(QRectF(dx + 6, iy, 3, item_h - 4), accent)
            # Item placeholder lines
            line_col = QColor(text)
            line_col.setAlpha(100 if i != 0 else 200)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(line_col)
            lw = sb_w * (0.5 + (i % 3) * 0.1)
            painter.drawRoundedRect(
                QRectF(dx + 16, iy + item_h * 0.35, lw - 20, 3), 1.5, 1.5,
            )

        # ---- Content area ---- #
        cx_start = dx + sb_w + 1
        content_w = dw - sb_w - 1
        content_y = dy + tb_h
        content_h = dh - tb_h - dh * 0.06

        # Content background
        painter.fillRect(QRectF(cx_start, content_y, content_w, content_h), bg)

        # Content blocks (cards)
        card_pad = 12
        card_w = (content_w - card_pad * 3) / 2
        card_h = (content_h - card_pad * 4) / 3

        for row in range(3):
            for col in range(2):
                cx = cx_start + card_pad + col * (card_w + card_pad)
                cy = content_y + card_pad + row * (card_h + card_pad)
                card_rect = QRectF(cx, cy, card_w, card_h)
                card_path = QPainterPath()
                card_path.addRoundedRect(card_rect, 6, 6)
                painter.fillPath(card_path, surface)

                # Header line in card
                hl_col = QColor(accent if (row + col) % 3 == 0 else text)
                hl_col.setAlpha(140)
                painter.setBrush(hl_col)
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawRoundedRect(
                    QRectF(cx + 8, cy + 8, card_w * 0.6, 3), 1.5, 1.5,
                )
                # Body lines
                body_col = QColor(text)
                body_col.setAlpha(60)
                painter.setBrush(body_col)
                for li in range(2):
                    lw = card_w * (0.8 - li * 0.15)
                    painter.drawRoundedRect(
                        QRectF(cx + 8, cy + 18 + li * 10, lw, 2.5), 1.2, 1.2,
                    )

        # ---- Taskbar ---- #
        taskbar_h = dh * 0.06
        taskbar_rect = QRectF(dx, dy + dh - taskbar_h, dw, taskbar_h)
        painter.fillRect(taskbar_rect, surface)

        # Taskbar dots
        n_dots = 5
        dot_spacing = dw / (n_dots + 1)
        for i in range(n_dots):
            tdx = dx + dot_spacing * (i + 1)
            tdy = taskbar_rect.y() + taskbar_h / 2
            r = taskbar_h * 0.2
            c = QColor(accent if i == 0 else text)
            c.setAlpha(200 if i == 0 else 80)
            painter.setBrush(c)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(QRectF(tdx - r, tdy - r, r * 2, r * 2))

        painter.setClipping(False)

        # ---- Theme label ---- #
        painter.setPen(QColor("#565f89"))
        label_font = QFont("Inter", 10)
        painter.setFont(label_font)
        painter.drawText(
            QRectF(0, h - 22, w, 20),
            Qt.AlignmentFlag.AlignCenter,
            self._theme,
        )

        painter.end()
