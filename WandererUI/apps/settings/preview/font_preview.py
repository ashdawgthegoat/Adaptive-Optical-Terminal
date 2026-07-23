"""
Typography specimen preview for font selection.

Renders the selected font at multiple sizes with a character set display
and a pangram, giving a clear impression of how the font looks.
"""

from __future__ import annotations

from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtGui import QColor, QFont, QPainter
from PyQt6.QtWidgets import QWidget


class FontPreview(QWidget):
    """Displays a typography specimen for the selected font."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._font_name = "Inter"
        self.setMinimumSize(300, 300)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def set_font(self, font_name: str) -> None:
        self._font_name = font_name
        self.update()

    # ------------------------------------------------------------------ #
    # Painting
    # ------------------------------------------------------------------ #

    def paintEvent(self, _event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)

        w, h = self.width(), self.height()
        bg = QColor("#1a1b26")
        text_primary = QColor("#c0caf5")
        text_muted = QColor("#565f89")
        accent = QColor("#7aa2f7")
        surface = QColor("#24283b")

        painter.fillRect(0, 0, w, h, bg)

        pad = 28
        y_cursor = float(pad)
        content_w = w - pad * 2

        # ---- Font name heading ---- #
        heading_font = QFont(self._font_name, 28)
        heading_font.setWeight(QFont.Weight.Bold)
        painter.setFont(heading_font)
        painter.setPen(accent)
        fm = painter.fontMetrics()
        painter.drawText(
            QRectF(pad, y_cursor, content_w, fm.height() + 4),
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
            self._font_name,
        )
        y_cursor += fm.height() + 16

        # Divider
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#3b4261"))
        painter.drawRect(QRectF(pad, y_cursor, content_w, 1))
        y_cursor += 16

        # ---- Uppercase ---- #
        label_font = QFont("Inter", 9)
        painter.setFont(label_font)
        painter.setPen(text_muted)
        painter.drawText(QRectF(pad, y_cursor, content_w, 14), Qt.AlignmentFlag.AlignLeft, "UPPERCASE")
        y_cursor += 18

        alpha_font = QFont(self._font_name, 16)
        painter.setFont(alpha_font)
        painter.setPen(text_primary)
        fm = painter.fontMetrics()
        upper_text = "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z"
        br = fm.boundingRect(QRectF(pad, y_cursor, content_w, 100).toRect(),
                             Qt.TextFlag.TextWordWrap, upper_text)
        painter.drawText(QRectF(pad, y_cursor, content_w, br.height() + 4),
                         Qt.TextFlag.TextWordWrap, upper_text)
        y_cursor += br.height() + 16

        # ---- Lowercase ---- #
        painter.setFont(label_font)
        painter.setPen(text_muted)
        painter.drawText(QRectF(pad, y_cursor, content_w, 14), Qt.AlignmentFlag.AlignLeft, "LOWERCASE")
        y_cursor += 18

        painter.setFont(alpha_font)
        painter.setPen(text_primary)
        lower_text = "a b c d e f g h i j k l m n o p q r s t u v w x y z"
        br = fm.boundingRect(QRectF(pad, y_cursor, content_w, 100).toRect(),
                             Qt.TextFlag.TextWordWrap, lower_text)
        painter.drawText(QRectF(pad, y_cursor, content_w, br.height() + 4),
                         Qt.TextFlag.TextWordWrap, lower_text)
        y_cursor += br.height() + 16

        # ---- Numbers ---- #
        painter.setFont(label_font)
        painter.setPen(text_muted)
        painter.drawText(QRectF(pad, y_cursor, content_w, 14), Qt.AlignmentFlag.AlignLeft, "NUMERALS")
        y_cursor += 18

        painter.setFont(alpha_font)
        painter.setPen(text_primary)
        painter.drawText(QRectF(pad, y_cursor, content_w, fm.height() + 4),
                         Qt.AlignmentFlag.AlignLeft, "0 1 2 3 4 5 6 7 8 9")
        y_cursor += fm.height() + 20

        # ---- Divider ---- #
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#3b4261"))
        painter.drawRect(QRectF(pad, y_cursor, content_w, 1))
        y_cursor += 16

        # ---- Pangram at multiple sizes ---- #
        pangram = "The quick brown fox jumps over the lazy dog"
        sizes = [
            ("36px", 24),
            ("24px", 18),
            ("16px", 13),
            ("12px", 10),
        ]

        for label, size in sizes:
            if y_cursor > h - 30:
                break
            # Size label
            painter.setFont(label_font)
            painter.setPen(text_muted)
            painter.drawText(QRectF(pad, y_cursor, content_w, 14), Qt.AlignmentFlag.AlignLeft, label)
            y_cursor += 16

            # Pangram
            sample_font = QFont(self._font_name, size)
            painter.setFont(sample_font)
            painter.setPen(text_primary)
            sfm = painter.fontMetrics()
            br = sfm.boundingRect(QRectF(pad, y_cursor, content_w, 100).toRect(),
                                  Qt.TextFlag.TextWordWrap, pangram)
            painter.drawText(QRectF(pad, y_cursor, content_w, br.height() + 4),
                             Qt.TextFlag.TextWordWrap, pangram)
            y_cursor += br.height() + 14

        painter.end()
