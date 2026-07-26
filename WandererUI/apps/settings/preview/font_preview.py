"""
Font preview for Wanderer Settings.

Renders the staged font package as a miniature Wanderer typography
specimen without mutating Maaya's live presentation state.
"""

from __future__ import annotations

from pathlib import Path
import importlib.util

from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtGui import QColor, QFont, QFontDatabase, QPainter
from PyQt6.QtWidgets import QSizePolicy, QWidget


class FontPreview(QWidget):
    """Displays the staged font using Wanderer's typography hierarchy."""

    def __init__(
        self,
        parent: QWidget | None = None
    ) -> None:

        super().__init__(parent)

        self.setFocusPolicy(
            Qt.FocusPolicy.NoFocus
        )

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        self._assets_root = Path("assets/fonts")

        self._font_package = ""
        self._font_family = "monospace"

        self._typography = {
            "title": 20,
            "section": 14,
            "body": 12,
            "footer": 11,
            "mono": 12,
        }

        # Keep successfully resolved packages cached so repeatedly moving
        # through Settings does not reload the same font file unnecessarily.
        self._font_cache: dict[str, tuple[str, dict[str, int]]] = {}

    # ============================================================
    # Public API
    # ============================================================

    def set_font(
        self,
        font_package: str
    ) -> None:
        """Preview a staged font package without changing Maaya."""

        if not font_package:
            return

        self._font_package = font_package

        family, typography = self._resolve_font(
            font_package
        )

        self._font_family = family
        self._typography = typography

        self.update()

    # ============================================================
    # Font resolution
    # ============================================================

    def _resolve_font(
        self,
        package: str
    ) -> tuple[str, dict[str, int]]:

        if package in self._font_cache:
            return self._font_cache[package]

        default_typography = {
            "title": 20,
            "section": 14,
            "body": 12,
            "footer": 11,
            "mono": 12,
        }

        folder = (
            self._assets_root
            / package
        )

        if not folder.exists():

            result = (
                package,
                default_typography
            )

            self._font_cache[package] = result

            return result

        # --------------------------------------------------------
        # Resolve font family
        # --------------------------------------------------------

        font_file = next(
            (
                file
                for file in folder.iterdir()
                if (
                    file.is_file()
                    and file.suffix.lower()
                    in {".ttf", ".otf"}
                )
            ),
            None
        )

        family = package

        if font_file is not None:

            font_id = (
                QFontDatabase.addApplicationFont(
                    str(font_file)
                )
            )

            if font_id != -1:

                families = (
                    QFontDatabase.applicationFontFamilies(
                        font_id
                    )
                )

                if families:
                    family = families[0]

        # --------------------------------------------------------
        # Resolve optional package typography
        # --------------------------------------------------------

        typography = default_typography.copy()

        typography_file = (
            folder
            / "typography.py"
        )

        if typography_file.exists():

            try:

                spec = (
                    importlib.util.spec_from_file_location(
                        f"settings_preview_fonts."
                        f"{package}.typography",
                        typography_file
                    )
                )

                if (
                    spec is not None
                    and spec.loader is not None
                ):

                    module = (
                        importlib.util.module_from_spec(
                            spec
                        )
                    )

                    spec.loader.exec_module(
                        module
                    )

                    typography_class = getattr(
                        module,
                        "Typography",
                        None
                    )

                    if typography_class is not None:

                        typography = {
                            "title": getattr(
                                typography_class,
                                "TITLE_SIZE",
                                20
                            ),
                            "section": getattr(
                                typography_class,
                                "SECTION_SIZE",
                                14
                            ),
                            "body": getattr(
                                typography_class,
                                "BODY_SIZE",
                                12
                            ),
                            "footer": getattr(
                                typography_class,
                                "FOOTER_SIZE",
                                11
                            ),
                            "mono": getattr(
                                typography_class,
                                "MONO_SIZE",
                                12
                            ),
                        }

            except Exception:
                # A broken optional typography file should not take
                # Settings down with it. Fall back to Wanderer defaults.
                typography = default_typography.copy()

        result = (
            family,
            typography
        )

        self._font_cache[package] = result

        return result

    # ============================================================
    # Painting
    # ============================================================

    def paintEvent(
        self,
        _event
    ) -> None:

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        painter.setRenderHint(
            QPainter.RenderHint.TextAntialiasing
        )

        width = self.width()
        height = self.height()

        # Temporary preview palette.
        #
        # ThemePreview will later establish the shared staged-theme
        # presentation contract for Settings.
        primary = QColor("#c0caf5")
        muted = QColor("#565f89")
        accent = QColor("#7aa2f7")
        divider = QColor("#3b4261")

        horizontal_pad = max(
            36,
            int(width * 0.07)
        )

        vertical_pad = max(
            36,
            int(height * 0.07)
        )

        content_width = (
            width
            - (horizontal_pad * 2)
        )

        y = float(vertical_pad)

        # --------------------------------------------------------
        # Wanderer title
        # --------------------------------------------------------

        title_font = self._make_font(
            self._typography["title"],
            QFont.Weight.Bold
        )

        painter.setFont(title_font)
        painter.setPen(accent)

        title_metrics = painter.fontMetrics()

        painter.drawText(
            QRectF(
                horizontal_pad,
                y,
                content_width,
                title_metrics.height()
            ),
            Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter,
            "WANDERER"
        )

        y += title_metrics.height() + 18

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(divider)

        painter.drawRect(
            QRectF(
                horizontal_pad,
                y,
                content_width,
                1
            )
        )

        y += 28

        # --------------------------------------------------------
        # Section typography
        # --------------------------------------------------------

        section_font = self._make_font(
            self._typography["section"],
            QFont.Weight.Bold
        )

        painter.setFont(section_font)
        painter.setPen(primary)

        section_metrics = painter.fontMetrics()

        painter.drawText(
            QRectF(
                horizontal_pad,
                y,
                content_width,
                section_metrics.height()
            ),
            Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter,
            "APPEARANCE"
        )

        y += section_metrics.height() + 22

        # --------------------------------------------------------
        # Body typography
        # --------------------------------------------------------

        body_font = self._make_font(
            self._typography["body"]
        )

        painter.setFont(body_font)
        painter.setPen(primary)

        body_metrics = painter.fontMetrics()

        body_text = (
            "The quick brown fox jumps over the lazy dog.\n"
            "Pack my box with five dozen liquor jugs."
        )

        body_height = (
            body_metrics.lineSpacing() * 2
            + 8
        )

        painter.drawText(
            QRectF(
                horizontal_pad,
                y,
                content_width,
                body_height
            ),
            Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignTop,
            body_text
        )

        y += body_height + 30

        # --------------------------------------------------------
        # Character specimen
        # --------------------------------------------------------

        label_font = self._make_font(
            self._typography["footer"]
        )

        painter.setFont(label_font)
        painter.setPen(muted)

        label_metrics = painter.fontMetrics()

        painter.drawText(
            QRectF(
                horizontal_pad,
                y,
                content_width,
                label_metrics.height()
            ),
            Qt.AlignmentFlag.AlignLeft,
            "CHARACTER SET"
        )

        y += label_metrics.height() + 12

        painter.setFont(body_font)
        painter.setPen(primary)

        character_lines = (
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ\n"
            "abcdefghijklmnopqrstuvwxyz\n"
            "0123456789"
        )

        character_height = (
            body_metrics.lineSpacing() * 3
            + 8
        )

        painter.drawText(
            QRectF(
                horizontal_pad,
                y,
                content_width,
                character_height
            ),
            Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignTop,
            character_lines
        )

        y += character_height + 30

        # --------------------------------------------------------
        # Navigation / mono specimen
        # --------------------------------------------------------

        painter.setFont(label_font)
        painter.setPen(muted)

        painter.drawText(
            QRectF(
                horizontal_pad,
                y,
                content_width,
                label_metrics.height()
            ),
            Qt.AlignmentFlag.AlignLeft,
            "NAVIGATION"
        )

        y += label_metrics.height() + 12

        mono_font = self._make_font(
            self._typography["mono"]
        )

        mono_font.setStyleHint(
            QFont.StyleHint.Monospace
        )

        painter.setFont(mono_font)
        painter.setPen(primary)

        mono_metrics = painter.fontMetrics()

        painter.drawText(
            QRectF(
                horizontal_pad,
                y,
                content_width,
                mono_metrics.height() + 6
            ),
            Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter,
            "↑  ↓  ←  →     ENTER     ESC     TAB"
        )

        # --------------------------------------------------------
        # Package identifier / footer typography
        # --------------------------------------------------------

        footer_font = self._make_font(
            self._typography["footer"]
        )

        painter.setFont(footer_font)
        painter.setPen(muted)

        footer_metrics = painter.fontMetrics()

        painter.drawText(
            QRectF(
                horizontal_pad,
                height
                - vertical_pad
                - footer_metrics.height(),
                content_width,
                footer_metrics.height()
            ),
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignVCenter,
            self._font_package
        )

        painter.end()

    # ============================================================
    # Helpers
    # ============================================================

    def _make_font(
        self,
        size: int,
        weight: QFont.Weight = QFont.Weight.Normal
    ) -> QFont:

        font = QFont(
            self._font_family,
            size
        )

        font.setWeight(weight)

        return font