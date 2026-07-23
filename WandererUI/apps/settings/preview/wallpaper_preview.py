"""
Wallpaper preview widget.

Paints procedural gradient wallpapers with decorative elements.
Each wallpaper is a unique painted composition using QPainter gradients.
"""

from __future__ import annotations

import math
import random

from PyQt6.QtCore import QPointF, QRectF, Qt
from PyQt6.QtGui import (
    QColor,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPen,
    QRadialGradient,
)
from PyQt6.QtWidgets import QWidget


class WallpaperPreview(QWidget):
    """Renders procedural wallpaper previews."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._wallpaper = "Midnight Gradient"
        self._star_seed = 42  # Fixed seed for deterministic stars
        self.setMinimumSize(300, 300)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def set_wallpaper(self, wallpaper_name: str) -> None:
        self._wallpaper = wallpaper_name
        self.update()

    # ------------------------------------------------------------------ #
    # Painting
    # ------------------------------------------------------------------ #

    def paintEvent(self, _event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w, h = self.width(), self.height()
        painter.fillRect(0, 0, w, h, QColor("#1a1b26"))

        # Preview area with monitor frame
        pad = 20
        pw, ph = w - pad * 2, h - pad * 2 - 20  # leave room for label
        px, py = float(pad), float(pad)

        # Outer frame
        frame = QPainterPath()
        frame.addRoundedRect(QRectF(px - 3, py - 3, pw + 6, ph + 6), 10, 10)
        painter.fillPath(frame, QColor("#3b4261"))

        # Clip to inner area
        inner = QRectF(px, py, pw, ph)
        clip = QPainterPath()
        clip.addRoundedRect(inner, 7, 7)
        painter.setClipPath(clip)

        dispatch = {
            "Midnight Gradient": self._paint_midnight,
            "Aurora Borealis": self._paint_aurora,
            "Deep Ocean": self._paint_ocean,
            "Nebula": self._paint_nebula,
            "Mountain Dusk": self._paint_mountain,
            "Cosmic Dust": self._paint_cosmic,
        }

        paint_fn = dispatch.get(self._wallpaper, self._paint_midnight)
        paint_fn(painter, px, py, pw, ph)

        painter.setClipping(False)

        # Label
        painter.setPen(QColor("#565f89"))
        from PyQt6.QtGui import QFont
        painter.setFont(QFont("Inter", 10))
        painter.drawText(
            QRectF(0, h - 22, w, 20),
            Qt.AlignmentFlag.AlignCenter,
            self._wallpaper,
        )

        painter.end()

    # ------------------------------------------------------------------ #
    # Individual wallpapers
    # ------------------------------------------------------------------ #

    def _paint_midnight(self, p: QPainter, x: float, y: float, w: float, h: float) -> None:
        grad = QLinearGradient(x, y, x, y + h)
        grad.setColorAt(0.0, QColor("#0f0c29"))
        grad.setColorAt(0.5, QColor("#302b63"))
        grad.setColorAt(1.0, QColor("#24243e"))
        p.fillRect(QRectF(x, y, w, h), grad)

        # Subtle radial glow
        glow = QRadialGradient(QPointF(x + w * 0.5, y + h * 0.35), w * 0.6)
        c = QColor("#7aa2f7")
        c.setAlpha(30)
        glow.setColorAt(0.0, c)
        c2 = QColor("#7aa2f7")
        c2.setAlpha(0)
        glow.setColorAt(1.0, c2)
        p.fillRect(QRectF(x, y, w, h), glow)

    def _paint_aurora(self, p: QPainter, x: float, y: float, w: float, h: float) -> None:
        # Base gradient
        grad = QLinearGradient(x, y, x, y + h)
        grad.setColorAt(0.0, QColor("#0f2027"))
        grad.setColorAt(0.5, QColor("#203a43"))
        grad.setColorAt(1.0, QColor("#2c5364"))
        p.fillRect(QRectF(x, y, w, h), grad)

        # Aurora bands
        p.setPen(Qt.PenStyle.NoPen)
        for i in range(5):
            band_y = y + h * (0.15 + i * 0.12)
            band_path = QPainterPath()
            band_path.moveTo(x, band_y)
            steps = 20
            for s in range(steps + 1):
                sx = x + (w / steps) * s
                sy = band_y + math.sin(s * 0.8 + i * 1.5) * h * 0.06
                band_path.lineTo(sx, sy)
            band_path.lineTo(x + w, y + h)
            band_path.lineTo(x, y + h)
            band_path.closeSubpath()

            colors = ["#73daca", "#9ece6a", "#7dcfff", "#bb9af7", "#7aa2f7"]
            c = QColor(colors[i % len(colors)])
            c.setAlpha(25 + i * 5)
            p.setBrush(c)
            p.drawPath(band_path)

        # Stars
        self._paint_stars(p, x, y, w, h, count=30, max_alpha=120)

    def _paint_ocean(self, p: QPainter, x: float, y: float, w: float, h: float) -> None:
        grad = QLinearGradient(x, y, x, y + h)
        grad.setColorAt(0.0, QColor("#000046"))
        grad.setColorAt(1.0, QColor("#1cb5e0"))
        p.fillRect(QRectF(x, y, w, h), grad)

        # Wave patterns
        p.setPen(Qt.PenStyle.NoPen)
        for i in range(4):
            wave_y = y + h * (0.55 + i * 0.1)
            wave = QPainterPath()
            wave.moveTo(x, wave_y)
            steps = 30
            for s in range(steps + 1):
                sx = x + (w / steps) * s
                sy = wave_y + math.sin(s * 0.5 + i * 2.0) * h * 0.03
                wave.lineTo(sx, sy)
            wave.lineTo(x + w, y + h)
            wave.lineTo(x, y + h)
            wave.closeSubpath()
            c = QColor("#1cb5e0")
            c.setAlpha(15 + i * 8)
            p.setBrush(c)
            p.drawPath(wave)

    def _paint_nebula(self, p: QPainter, x: float, y: float, w: float, h: float) -> None:
        grad = QLinearGradient(x, y, x + w, y + h)
        grad.setColorAt(0.0, QColor("#141e30"))
        grad.setColorAt(0.5, QColor("#6b2fa0"))
        grad.setColorAt(1.0, QColor("#e44d26"))
        p.fillRect(QRectF(x, y, w, h), grad)

        # Nebula glow spots
        spots = [
            (0.3, 0.4, 0.3, "#bb9af7", 35),
            (0.7, 0.6, 0.25, "#f7768e", 30),
            (0.5, 0.3, 0.2, "#e0af68", 25),
        ]
        for sx, sy, sr, color, alpha in spots:
            glow = QRadialGradient(QPointF(x + w * sx, y + h * sy), w * sr)
            c = QColor(color)
            c.setAlpha(alpha)
            glow.setColorAt(0.0, c)
            c2 = QColor(color)
            c2.setAlpha(0)
            glow.setColorAt(1.0, c2)
            p.fillRect(QRectF(x, y, w, h), glow)

        self._paint_stars(p, x, y, w, h, count=60, max_alpha=200)

    def _paint_mountain(self, p: QPainter, x: float, y: float, w: float, h: float) -> None:
        # Sky gradient
        grad = QLinearGradient(x, y, x, y + h)
        grad.setColorAt(0.0, QColor("#e94560"))
        grad.setColorAt(0.3, QColor("#16213e"))
        grad.setColorAt(1.0, QColor("#1a1a2e"))
        p.fillRect(QRectF(x, y, w, h), grad)

        # Sun/glow
        sun = QRadialGradient(QPointF(x + w * 0.5, y + h * 0.35), w * 0.25)
        sc = QColor("#e94560")
        sc.setAlpha(60)
        sun.setColorAt(0.0, sc)
        sc2 = QColor("#e94560")
        sc2.setAlpha(0)
        sun.setColorAt(1.0, sc2)
        p.fillRect(QRectF(x, y, w, h), sun)

        # Mountain silhouettes (3 layers)
        mountains = [
            (0.55, [(0, 0.9), (0.15, 0.55), (0.35, 0.7), (0.5, 0.45), (0.65, 0.65), (0.85, 0.5), (1.0, 0.85)], "#0a0a1a"),
            (0.65, [(0, 0.95), (0.2, 0.65), (0.4, 0.75), (0.55, 0.6), (0.75, 0.7), (0.9, 0.62), (1.0, 0.9)], "#10101e"),
            (0.75, [(0, 1.0), (0.1, 0.78), (0.3, 0.82), (0.5, 0.72), (0.7, 0.8), (0.85, 0.75), (1.0, 0.95)], "#161628"),
        ]
        p.setPen(Qt.PenStyle.NoPen)
        for _base_y, points, color in mountains:
            mt = QPainterPath()
            mt.moveTo(x, y + h)
            for px_frac, py_frac in points:
                mt.lineTo(x + w * px_frac, y + h * py_frac)
            mt.lineTo(x + w, y + h)
            mt.closeSubpath()
            p.setBrush(QColor(color))
            p.drawPath(mt)

        self._paint_stars(p, x, y, w, h * 0.5, count=25, max_alpha=150)

    def _paint_cosmic(self, p: QPainter, x: float, y: float, w: float, h: float) -> None:
        grad = QLinearGradient(x, y, x, y + h)
        grad.setColorAt(0.0, QColor("#0a0a0a"))
        grad.setColorAt(0.5, QColor("#1a0a2e"))
        grad.setColorAt(1.0, QColor("#2d1b69"))
        p.fillRect(QRectF(x, y, w, h), grad)

        # Cosmic dust clouds
        dust = [
            (0.3, 0.5, 0.4, "#bb9af7", 20),
            (0.7, 0.4, 0.35, "#7aa2f7", 15),
        ]
        for dx, dy, dr, color, alpha in dust:
            glow = QRadialGradient(QPointF(x + w * dx, y + h * dy), w * dr)
            c = QColor(color)
            c.setAlpha(alpha)
            glow.setColorAt(0.0, c)
            c2 = QColor(color)
            c2.setAlpha(0)
            glow.setColorAt(1.0, c2)
            p.fillRect(QRectF(x, y, w, h), glow)

        self._paint_stars(p, x, y, w, h, count=80, max_alpha=220)

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #

    def _paint_stars(
        self,
        p: QPainter,
        x: float, y: float, w: float, h: float,
        count: int = 40,
        max_alpha: int = 180,
    ) -> None:
        """Paint deterministic scattered stars."""
        rng = random.Random(self._star_seed)
        p.setPen(Qt.PenStyle.NoPen)
        for _ in range(count):
            sx = x + rng.random() * w
            sy = y + rng.random() * h
            sr = rng.uniform(0.5, 2.0)
            alpha = rng.randint(60, max_alpha)
            c = QColor(255, 255, 255, alpha)
            p.setBrush(c)
            p.drawEllipse(QRectF(sx - sr, sy - sr, sr * 2, sr * 2))
