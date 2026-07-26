"""
Wallpaper preview widget.

Renders real Wanderer wallpaper assets without modifying
Maaya's active wallpaper state.
"""

from pathlib import Path

from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtGui import (
    QColor,
    QFont,
    QPainter,
    QPainterPath,
    QPixmap,
)
from PyQt6.QtWidgets import QWidget, QSizePolicy


class WallpaperPreview(QWidget):

    WALLPAPER_ROOT = Path("assets/wallpapers")

    def __init__(
        self,
        parent: QWidget | None = None
    ) -> None:

        super().__init__(parent)

        self._wallpaper = ""
        self._wallpaper_path = None

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        self.setMinimumSize(0, 0)
        self.setFocusPolicy(
            Qt.FocusPolicy.NoFocus
        )

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def set_wallpaper(
        self,
        wallpaper_name: str
    ) -> None:

        self._wallpaper = wallpaper_name
        self._wallpaper_path = (
            self._find_wallpaper(wallpaper_name)
        )

        self.update()

    # ---------------------------------------------------------
    # Asset resolution
    # ---------------------------------------------------------

    def _find_wallpaper(
        self,
        wallpaper_name: str
    ) -> Path | None:

        if not wallpaper_name:
            return None

        if not self.WALLPAPER_ROOT.exists():
            return None

        for path in self.WALLPAPER_ROOT.rglob(
            wallpaper_name
        ):
            if path.is_file():
                return path

        return None

    # ---------------------------------------------------------
    # Painting
    # ---------------------------------------------------------

    def paintEvent(self, _event) -> None:

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        w = self.width()
        h = self.height()

        # ---------------------------------------------------------
        # Preview background
        # ---------------------------------------------------------

        painter.fillRect(
            self.rect(),
            QColor("#000000")
        )

        # ---------------------------------------------------------
        # Simulated Wanderer viewport
        #
        # Use most of the available PreviewPanel while preserving
        # some breathing room around the miniature viewport.
        # ---------------------------------------------------------

        horizontal_margin = max(
            32,
            int(w * 0.08)
        )

        vertical_margin = max(
            32,
            int(h * 0.10)
        )

        label_height = 28

        viewport_rect = QRectF(
            horizontal_margin,
            vertical_margin,
            w - (horizontal_margin * 2),
            h - (vertical_margin * 2) - label_height
        )

        # ---------------------------------------------------------
        # Viewport frame
        # ---------------------------------------------------------

        frame = QPainterPath()

        frame.addRoundedRect(
            viewport_rect,
            8,
            8
        )

        painter.fillPath(
            frame,
            QColor("#202020")
        )

        # Small inset representing the real viewport content area.

        content_rect = viewport_rect.adjusted(
            12,
            12,
            -12,
            -12
        )

        content_clip = QPainterPath()

        content_clip.addRoundedRect(
            content_rect,
            5,
            5
        )

        painter.setClipPath(
            content_clip
        )

        painter.fillRect(
            content_rect,
            QColor("#000000")
        )

        # ---------------------------------------------------------
        # Wallpaper
        # ---------------------------------------------------------

        self._paint_wallpaper(
            painter,
            content_rect
        )

        painter.setClipping(False)

        # ---------------------------------------------------------
        # Wallpaper identifier
        # ---------------------------------------------------------

        painter.setPen(
            QColor("#808080")
        )

        painter.setFont(
            QFont("monospace", 10)
        )

        painter.drawText(
            QRectF(
                0,
                viewport_rect.bottom() + 8,
                w,
                label_height
            ),
            Qt.AlignmentFlag.AlignCenter,
            self._wallpaper
        )

        painter.end()

    # ---------------------------------------------------------
    # Wallpaper rendering
    # ---------------------------------------------------------

    def _paint_wallpaper(
        self,
        painter: QPainter,
        rect: QRectF
    ) -> None:

        path = self._wallpaper_path

        if path is None:
            self._paint_missing(
                painter,
                rect
            )
            return

        suffix = path.suffix.lower()

        if suffix == ".txt":

            self._paint_ascii(
                painter,
                rect,
                path
            )

        elif suffix in {
            ".png",
            ".jpg",
            ".jpeg",
            ".webp"
        }:

            self._paint_image(
                painter,
                rect,
                path
            )

        else:

            self._paint_missing(
                painter,
                rect
            )

    # ---------------------------------------------------------
    # ASCII
    # ---------------------------------------------------------

    def _paint_ascii(
        self,
        painter: QPainter,
        rect: QRectF,
        path: Path
    ) -> None:

        try:
            text = path.read_text(
                encoding="utf-8"
            )

        except Exception:

            self._paint_missing(
                painter,
                rect
            )

            return

        lines = text.splitlines()

        if not lines:
            return

        # ---------------------------------------------------------
        # Simulate the real Viewport's typography.
        #
        # The actual AsciiRenderer uses Maaya's BODY_SIZE and
        # centers the QLabel. Preview uses a proportional miniature
        # equivalent instead of forcing the entire ASCII file to
        # fit into the available rectangle.
        # ---------------------------------------------------------

        reference_height = 700.0
        reference_font_size = 14.0

        scale = (
            rect.height()
            / reference_height
        )

        font_size = max(
            5.0,
            reference_font_size * scale
        )

        font = QFont(
            "monospace"
        )

        font.setStyleHint(
            QFont.StyleHint.Monospace
        )

        font.setPointSizeF(
            font_size
        )

        painter.setFont(font)

        painter.setPen(
            QColor("#d0d0d0")
        )

        painter.drawText(
            rect,
            Qt.AlignmentFlag.AlignCenter,
            text
        )

    # ---------------------------------------------------------
    # Image
    # ---------------------------------------------------------

    def _paint_image(
        self,
        painter: QPainter,
        rect: QRectF,
        path: Path
    ) -> None:

        pixmap = QPixmap(
            str(path)
        )

        if pixmap.isNull():
            self._paint_missing(
                painter,
                rect
            )
            return

        scaled = pixmap.scaled(
            int(rect.width()),
            int(rect.height()),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        x = (
            rect.x()
            + (
                rect.width()
                - scaled.width()
            ) / 2
        )

        y = (
            rect.y()
            + (
                rect.height()
                - scaled.height()
            ) / 2
        )

        painter.drawPixmap(
            int(x),
            int(y),
            scaled
        )

    # ---------------------------------------------------------
    # Fallback
    # ---------------------------------------------------------

    def _paint_missing(
        self,
        painter: QPainter,
        rect: QRectF
    ) -> None:

        painter.setPen(
            QColor("#666666")
        )

        painter.setFont(
            QFont("monospace", 10)
        )

        painter.drawText(
            rect,
            Qt.AlignmentFlag.AlignCenter,
            "Preview unavailable"
        )