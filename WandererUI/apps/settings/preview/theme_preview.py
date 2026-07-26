"""
Theme preview for Wanderer Settings.

Renders a miniature schematic representation of the Wanderer desktop
using the staged theme package.

The preview deliberately contains no readable interface text, wallpaper,
or selected Wanderer font. Its only responsibility is to visualise the
theme's own presentation language.
"""

from __future__ import annotations

from pathlib import Path
import importlib.util

from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtGui import QColor, QPainter, QPen
from PyQt6.QtWidgets import QSizePolicy, QWidget


class ThemePreview(QWidget):
    """Visualises a staged Wanderer theme without mutating Maaya."""

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

        self._assets_root = Path("assets/themes")

        self._theme_package = ""

        self._theme = self._default_theme()

        self._theme_cache: dict[str, dict] = {}

    # ============================================================
    # Public API
    # ============================================================

    def set_theme(
        self,
        theme_package: str
    ) -> None:
        """Preview a staged theme package."""

        if not theme_package:
            return

        self._theme_package = theme_package

        self._theme = self._resolve_theme(
            theme_package
        )

        self.update()

    # ============================================================
    # Theme resolution
    # ============================================================

    def _default_theme(self) -> dict:
        """Return safe fallback values matching Wanderer's theme schema."""

        return {
            "palette": {
                "background": "#000000",
                "surface": "#111111",
                "primary": "#ffffff",
                "secondary": "#888888",
                "accent": "#a32626",
                "success": "#5f875f",
                "warning": "#af875f",
                "error": "#af5f5f",
                "separator": "#444444",
            },
            "spacing": {
                "outer_margin": 12,
                "inner_margin": 8,
                "section_spacing": 12,
                "item_spacing": 6,
            },
            "borders": {
                "padding": 8,
                "width": 1,
                "active_width": 2,
                "radius": 0,
            },
            "information": {
                "style": "bar",
                "bar_length": 10,
                "filled": "█",
                "empty": "░",
            },
        }

    def _resolve_theme(
        self,
        package: str
    ) -> dict:
        """Read a theme definition without applying it through Maaya."""

        if package in self._theme_cache:
            return self._theme_cache[package]

        definition_file = (
            self._assets_root
            / package
            / "definition.py"
        )

        if not definition_file.exists():
            return self._default_theme()

        try:

            spec = importlib.util.spec_from_file_location(
                f"settings_preview_themes.{package}.definition",
                definition_file
            )

            if (
                spec is None
                or spec.loader is None
            ):
                return self._default_theme()

            module = importlib.util.module_from_spec(
                spec
            )

            spec.loader.exec_module(
                module
            )

            palette = getattr(
                module,
                "Palette",
                None
            )

            spacing = getattr(
                module,
                "Spacing",
                None
            )

            borders = getattr(
                module,
                "Borders",
                None
            )

            information = getattr(
                module,
                "Information",
                None
            )

            defaults = self._default_theme()

            theme = {
                "palette": {
                    "background": getattr(
                        palette,
                        "BACKGROUND",
                        defaults["palette"]["background"]
                    ),
                    "surface": getattr(
                        palette,
                        "SURFACE",
                        defaults["palette"]["surface"]
                    ),
                    "primary": getattr(
                        palette,
                        "PRIMARY",
                        defaults["palette"]["primary"]
                    ),
                    "secondary": getattr(
                        palette,
                        "SECONDARY",
                        defaults["palette"]["secondary"]
                    ),
                    "accent": getattr(
                        palette,
                        "ACCENT",
                        defaults["palette"]["accent"]
                    ),
                    "success": getattr(
                        palette,
                        "SUCCESS",
                        defaults["palette"]["success"]
                    ),
                    "warning": getattr(
                        palette,
                        "WARNING",
                        defaults["palette"]["warning"]
                    ),
                    "error": getattr(
                        palette,
                        "ERROR",
                        defaults["palette"]["error"]
                    ),
                    "separator": getattr(
                        palette,
                        "SEPARATOR",
                        defaults["palette"]["separator"]
                    ),
                },
                "spacing": {
                    "outer_margin": getattr(
                        spacing,
                        "OUTER_MARGIN",
                        defaults["spacing"]["outer_margin"]
                    ),
                    "inner_margin": getattr(
                        spacing,
                        "INNER_MARGIN",
                        defaults["spacing"]["inner_margin"]
                    ),
                    "section_spacing": getattr(
                        spacing,
                        "SECTION_SPACING",
                        defaults["spacing"]["section_spacing"]
                    ),
                    "item_spacing": getattr(
                        spacing,
                        "ITEM_SPACING",
                        defaults["spacing"]["item_spacing"]
                    ),
                },
                "borders": {
                    "padding": getattr(
                        borders,
                        "PADDING",
                        defaults["borders"]["padding"]
                    ),
                    "width": getattr(
                        borders,
                        "WIDTH",
                        defaults["borders"]["width"]
                    ),
                    "active_width": getattr(
                        borders,
                        "ACTIVE_WIDTH",
                        defaults["borders"]["active_width"]
                    ),
                    "radius": getattr(
                        borders,
                        "RADIUS",
                        defaults["borders"]["radius"]
                    ),
                },
                "information": {
                    "style": getattr(
                        information,
                        "STYLE",
                        defaults["information"]["style"]
                    ),
                    "bar_length": getattr(
                        information,
                        "BAR_LENGTH",
                        defaults["information"]["bar_length"]
                    ),
                    "filled": getattr(
                        information,
                        "FILLED",
                        defaults["information"]["filled"]
                    ),
                    "empty": getattr(
                        information,
                        "EMPTY",
                        defaults["information"]["empty"]
                    ),
                },
            }

        except Exception as exc:

            print(
                "[ThemePreview] Failed to load",
                package,
                exc
            )

            return self._default_theme()

        self._theme_cache[package] = theme

        return theme

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

        palette = self._theme["palette"]
        spacing = self._theme["spacing"]
        borders = self._theme["borders"]

        background = QColor(
            palette["background"]
        )

        surface = QColor(
            palette["surface"]
        )

        primary = QColor(
            palette["primary"]
        )

        secondary = QColor(
            palette["secondary"]
        )

        accent = QColor(
            palette["accent"]
        )

        success = QColor(
            palette["success"]
        )

        warning = QColor(
            palette["warning"]
        )

        error = QColor(
            palette["error"]
        )

        separator = QColor(
            palette["separator"]
        )

        # The ThemePreview itself remains transparent.
        # Only Mini-Wanderer receives the staged theme background.

        width = float(self.width())
        height = float(self.height())

        outer = max(
            30.0,
            min(width, height) * 0.07
        )

        desktop = QRectF(
            outer,
            outer,
            width - (outer * 2),
            height - (outer * 2)
        )

        if (
            desktop.width() <= 0
            or desktop.height() <= 0
        ):
            painter.end()
            return

        radius = max(
            0.0,
            float(borders["radius"])
        )

        # --------------------------------------------------------
        # Miniature desktop shell
        # --------------------------------------------------------

        painter.setPen(
            QPen(
                separator,
                max(
                    1,
                    int(borders["width"])
                )
            )
        )

        painter.setBrush(
            background
        )

        painter.drawRoundedRect(
            desktop,
            radius,
            radius
        )

        # Scale the theme's spacing values into the miniature.
        #
        # We preserve their relative effect without assuming that theme
        # pixels should map literally into preview pixels.

        base_outer = max(
            1.0,
            float(spacing["outer_margin"])
        )

        base_inner = max(
            1.0,
            float(spacing["inner_margin"])
        )

        base_section = max(
            1.0,
            float(spacing["section_spacing"])
        )

        base_item = max(
            1.0,
            float(spacing["item_spacing"])
        )

        shell_pad = max(
            12.0,
            min(
                28.0,
                base_outer * 1.5
            )
        )

        panel_gap = max(
            8.0,
            min(
                24.0,
                base_section
            )
        )

        inner_pad = max(
            8.0,
            min(
                20.0,
                base_inner
            )
        )

        item_gap = max(
            5.0,
            min(
                14.0,
                base_item
            )
        )

        content = desktop.adjusted(
            shell_pad,
            shell_pad,
            -shell_pad,
            -shell_pad
        )

        # --------------------------------------------------------
        # Top chrome
        # --------------------------------------------------------

        top_height = max(
            32.0,
            content.height() * 0.075
        )

        top_rect = QRectF(
            content.left(),
            content.top(),
            content.width(),
            top_height
        )

        self._draw_top_chrome(
            painter,
            top_rect,
            primary,
            secondary,
            accent,
            separator
        )

        # --------------------------------------------------------
        # Footer chrome
        # --------------------------------------------------------

        footer_height = max(
            28.0,
            content.height() * 0.065
        )

        footer_rect = QRectF(
            content.left(),
            content.bottom() - footer_height,
            content.width(),
            footer_height
        )

        self._draw_footer(
            painter,
            footer_rect,
            primary,
            secondary,
            accent,
            separator
        )

        # --------------------------------------------------------
        # Main three-panel desktop
        # --------------------------------------------------------

        panels_top = (
            top_rect.bottom()
            + panel_gap
        )

        panels_bottom = (
            footer_rect.top()
            - panel_gap
        )

        panels_height = (
            panels_bottom
            - panels_top
        )

        panels_width = content.width()

        navigation_width = (
            panels_width * 0.22
        )

        context_width = (
            panels_width * 0.24
        )

        viewport_width = (
            panels_width
            - navigation_width
            - context_width
            - (panel_gap * 2)
        )

        navigation_rect = QRectF(
            content.left(),
            panels_top,
            navigation_width,
            panels_height
        )

        viewport_rect = QRectF(
            navigation_rect.right()
            + panel_gap,
            panels_top,
            viewport_width,
            panels_height
        )

        context_rect = QRectF(
            viewport_rect.right()
            + panel_gap,
            panels_top,
            context_width,
            panels_height
        )

        self._draw_navigation(
            painter,
            navigation_rect,
            background,
            surface,
            primary,
            secondary,
            accent,
            separator,
            borders,
            radius,
            inner_pad,
            item_gap
        )

        self._draw_viewport(
            painter,
            viewport_rect,
            background,
            surface,
            primary,
            secondary,
            accent,
            separator,
            borders,
            radius
        )

        self._draw_context(
            painter,
            context_rect,
            background,
            surface,
            primary,
            secondary,
            accent,
            success,
            warning,
            error,
            separator,
            borders,
            radius,
            inner_pad,
            item_gap
        )

        painter.end()

    # ============================================================
    # Mini-Wanderer regions
    # ============================================================

    def _draw_top_chrome(
        self,
        painter: QPainter,
        rect: QRectF,
        primary: QColor,
        secondary: QColor,
        accent: QColor,
        separator: QColor
    ) -> None:

        borders = self._theme["borders"]

        self._panel(
            painter,
            rect,
            QColor(
                self._theme["palette"]["background"]
            ),
            separator,
            borders["width"],
            borders["radius"]
        )

        bar_height = max(
            4.0,
            rect.height() * 0.16
        )

        self._bar(
            painter,
            QRectF(
                rect.left(),
                rect.center().y() - bar_height / 2,
                rect.width() * 0.15,
                bar_height
            ),
            primary
        )

        self._bar(
            painter,
            QRectF(
                rect.center().x() - rect.width() * 0.07,
                rect.center().y() - bar_height / 2,
                rect.width() * 0.14,
                bar_height
            ),
            secondary
        )

        icon_size = max(
            7.0,
            rect.height() * 0.24
        )

        icon_gap = icon_size * 0.8

        start_x = (
            rect.right()
            - (icon_size * 3)
            - (icon_gap * 2)
        )

        for index, color in enumerate(
            (
                secondary,
                accent,
                primary
            )
        ):

            x = (
                start_x
                + index * (icon_size + icon_gap)
            )

            painter.setPen(
                Qt.PenStyle.NoPen
            )

            painter.setBrush(
                color
            )

            painter.drawEllipse(
                QRectF(
                    x,
                    rect.center().y()
                    - icon_size / 2,
                    icon_size,
                    icon_size
                )
            )

    def _draw_navigation(
        self,
        painter: QPainter,
        rect: QRectF,
        background: QColor,
        surface: QColor,
        primary: QColor,
        secondary: QColor,
        accent: QColor,
        separator: QColor,
        borders: dict,
        radius: float,
        inner_pad: float,
        item_gap: float
    ) -> None:

        self._panel(
            painter,
            rect,
            background,
            separator,
            borders["width"],
            radius
        )

        content = rect.adjusted(
            inner_pad,
            inner_pad,
            -inner_pad,
            -inner_pad
        )

        heading_height = max(
            5.0,
            rect.height() * 0.018
        )

        self._bar(
            painter,
            QRectF(
                content.left(),
                content.top(),
                content.width() * 0.58,
                heading_height
            ),
            primary
        )

        y = (
            content.top()
            + heading_height
            + item_gap * 3
        )

        row_height = max(
            20.0,
            rect.height() * 0.075
        )

        row_widths = (
            0.70,
            0.52,
            0.62,
            0.45,
            0.58,
        )

        for index, width_factor in enumerate(
            row_widths
        ):

            row = QRectF(
                content.left(),
                y,
                content.width(),
                row_height
            )

            if index == 0:

                painter.setPen(
                    QPen(
                        accent,
                        max(
                            1,
                            int(
                                borders[
                                    "active_width"
                                ]
                            )
                        )
                    )
                )

                painter.setBrush(
                    surface
                )

                painter.drawRoundedRect(
                    row,
                    radius,
                    radius
                )

                indicator_width = max(
                    3.0,
                    row.width() * 0.025
                )

                self._bar(
                    painter,
                    QRectF(
                        row.left(),
                        row.top(),
                        indicator_width,
                        row.height()
                    ),
                    accent
                )

                bar_color = primary

            else:
                bar_color = secondary

            bar_height = max(
                4.0,
                row.height() * 0.16
            )

            self._bar(
                painter,
                QRectF(
                    row.left()
                    + inner_pad,
                    row.center().y()
                    - bar_height / 2,
                    max(
                        8.0,
                        (
                            row.width()
                            - inner_pad * 2
                        )
                        * width_factor
                    ),
                    bar_height
                ),
                bar_color
            )

            y += (
                row_height
                + item_gap
            )

    def _draw_viewport(
        self,
        painter: QPainter,
        rect: QRectF,
        background: QColor,
        surface: QColor,
        primary: QColor,
        secondary: QColor,
        accent: QColor,
        separator: QColor,
        borders: dict,
        radius: float
    ) -> None:

        self._panel(
            painter,
            rect,
            background,
            accent,
            borders["active_width"],
            radius
        )

        # A schematic composition rather than wallpaper or typography.
        # This deliberately belongs only to ThemePreview.

        center = rect.center()

        face_size = min(
                rect.width(),
                rect.height()
                ) * 0.22

        face_rect = QRectF(
            center.x() - face_size / 2,
            center.y() - face_size / 2,
            face_size,
            face_size
        )

        # Face outline
        painter.setPen(
            QPen(
                primary,
                max(
                    2,
                    int(borders["width"]) + 1
                )
            )
        )

        painter.setBrush(
            Qt.BrushStyle.NoBrush
        )

        painter.drawEllipse(
            face_rect
        )

        # Eyes
        eye_size = max(
            4.0,
            face_size * 0.07
        )

        eye_y = (
            center.y()
            - face_size * 0.12
        )

        eye_offset = (
            face_size * 0.18
        )

        painter.setPen(
            Qt.PenStyle.NoPen
        )

        painter.setBrush(
            accent
        )

        painter.drawRect(
            QRectF(
                center.x()
                - eye_offset
                - eye_size / 2,
                eye_y,
                eye_size,
                eye_size
            )
        )

        painter.drawRect(
            QRectF(
                center.x()
                + eye_offset
                - eye_size / 2,
                eye_y,
                eye_size,
                eye_size
            )
        )

        # Smile
        painter.setPen(
            QPen(
                secondary,
                max(
                    2,
                    int(borders["width"]) + 1
                )
            )
        )

        painter.setBrush(
            Qt.BrushStyle.NoBrush
        )

        smile_rect = QRectF(
            center.x() - face_size * 0.25,
            center.y() - face_size * 0.02,
            face_size * 0.50,
            face_size * 0.32
        )

        painter.drawArc(
            smile_rect,
            180 * 16,
            180 * 16
        )

        # Small surface specimen.

        specimen_width = (
            rect.width() * 0.18
        )

        specimen_height = (
            rect.height() * 0.07
        )

        specimen = QRectF(
            rect.center().x()
            - specimen_width / 2,
            rect.bottom()
            - specimen_height
            - rect.height() * 0.10,
            specimen_width,
            specimen_height
        )

        painter.setPen(
            QPen(
                separator,
                max(
                    1,
                    int(borders["width"])
                )
            )
        )

        painter.setBrush(
            surface
        )

        painter.drawRoundedRect(
            specimen,
            radius,
            radius
        )

    def _draw_context(
        self,
        painter: QPainter,
        rect: QRectF,
        background: QColor,
        surface: QColor,
        primary: QColor,
        secondary: QColor,
        accent: QColor,
        success: QColor,
        warning: QColor,
        error: QColor,
        separator: QColor,
        borders: dict,
        radius: float,
        inner_pad: float,
        item_gap: float
    ) -> None:

        self._panel(
            painter,
            rect,
            background,
            separator,
            borders["width"],
            radius
        )

        content = rect.adjusted(
            inner_pad,
            inner_pad,
            -inner_pad,
            -inner_pad
        )

        heading_height = max(
            5.0,
            rect.height() * 0.018
        )

        self._bar(
            painter,
            QRectF(
                content.left(),
                content.top(),
                content.width() * 0.62,
                heading_height
            ),
            primary
        )

        y = (
            content.top()
            + heading_height
            + item_gap * 3
        )

        # Information bars

        for ratio in (
            0.68,
            0.43
        ):

            label_height = max(
                4.0,
                rect.height() * 0.012
            )

            self._bar(
                painter,
                QRectF(
                    content.left(),
                    y,
                    content.width() * 0.38,
                    label_height
                ),
                secondary
            )

            y += (
                label_height
                + item_gap
            )

            self._information_bar(
                painter,
                QRectF(
                    content.left(),
                    y,
                    content.width(),
                    max(
                        8.0,
                        rect.height() * 0.025
                    )
                ),
                ratio,
                accent,
                surface
            )

            y += (
                rect.height() * 0.085
            )

        # Separator

        self._line(
            painter,
            content.left(),
            y,
            content.right(),
            y,
            separator,
            1
        )

        y += (
            item_gap * 3
        )

        # Status indicators: success / warning / error

        indicator_size = max(
            8.0,
            rect.width() * 0.055
        )

        indicator_gap = (
            content.width()
            - indicator_size * 3
        ) / 2

        for index, color in enumerate(
            (
                success,
                warning,
                error
            )
        ):

            x = (
                content.left()
                + index
                * (
                    indicator_size
                    + indicator_gap
                )
            )

            painter.setPen(
                Qt.PenStyle.NoPen
            )

            painter.setBrush(
                color
            )

            painter.drawEllipse(
                QRectF(
                    x,
                    y,
                    indicator_size,
                    indicator_size
                )
            )

        y += (
            indicator_size
            + item_gap * 4
        )

        # Secondary surface block

        surface_rect = QRectF(
            content.left(),
            y,
            content.width(),
            max(
                30.0,
                rect.height() * 0.12
            )
        )

        painter.setPen(
            QPen(
                separator,
                max(
                    1,
                    int(borders["width"])
                )
            )
        )

        painter.setBrush(
            surface
        )

        painter.drawRoundedRect(
            surface_rect,
            radius,
            radius
        )

    def _draw_footer(
        self,
        painter: QPainter,
        rect: QRectF,
        primary: QColor,
        secondary: QColor,
        accent: QColor,
        separator: QColor
    ) -> None:

        borders = self._theme["borders"]

        self._panel(
            painter,
            rect,
            QColor(
                self._theme["palette"]["background"]
            ),
            separator,
            borders["width"],
            borders["radius"]
        )

        bar_height = max(
            4.0,
            rect.height() * 0.16
        )

        self._bar(
            painter,
            QRectF(
                rect.left(),
                rect.center().y()
                - bar_height / 2,
                rect.width() * 0.18,
                bar_height
            ),
            secondary
        )

        self._bar(
            painter,
            QRectF(
                rect.center().x()
                - rect.width() * 0.08,
                rect.center().y()
                - bar_height / 2,
                rect.width() * 0.16,
                bar_height
            ),
            primary
        )

        self._bar(
            painter,
            QRectF(
                rect.right()
                - rect.width() * 0.11,
                rect.center().y()
                - bar_height / 2,
                rect.width() * 0.11,
                bar_height
            ),
            accent
        )

    # ============================================================
    # Primitive drawing helpers
    # ============================================================

    def _panel(
        self,
        painter: QPainter,
        rect: QRectF,
        fill: QColor,
        border: QColor,
        width: int,
        radius: float
    ) -> None:

        painter.setPen(
            QPen(
                border,
                max(
                    1,
                    int(width)
                )
            )
        )

        painter.setBrush(
            fill
        )

        painter.drawRoundedRect(
            rect,
            radius,
            radius
        )

    def _bar(
        self,
        painter: QPainter,
        rect: QRectF,
        color: QColor
    ) -> None:

        painter.setPen(
            Qt.PenStyle.NoPen
        )

        painter.setBrush(
            color
        )

        radius = max(
            0.0,
            float(
                self._theme["borders"]["radius"]
            )
        )

        painter.drawRoundedRect(
            rect,
            radius,
            radius
        )

    def _line(
        self,
        painter: QPainter,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        color: QColor,
        width: int
    ) -> None:

        painter.setPen(
            QPen(
                color,
                max(
                    1,
                    int(width)
                )
            )
        )

        painter.drawLine(
            int(x1),
            int(y1),
            int(x2),
            int(y2)
        )

    def _information_bar(
        self,
        painter: QPainter,
        rect: QRectF,
        ratio: float,
        filled: QColor,
        empty: QColor
    ) -> None:

        ratio = max(
            0.0,
            min(
                1.0,
                ratio
            )
        )

        painter.setPen(
            Qt.PenStyle.NoPen
        )

        painter.setBrush(
            empty
        )

        painter.drawRoundedRect(
            rect,
            rect.height() / 2,
            rect.height() / 2
        )

        filled_rect = QRectF(
            rect.left(),
            rect.top(),
            rect.width() * ratio,
            rect.height()
        )

        painter.setBrush(
            filled
        )

        painter.drawRoundedRect(
            filled_rect,
            rect.height() / 2,
            rect.height() / 2
        )