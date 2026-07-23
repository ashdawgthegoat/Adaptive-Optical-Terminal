"""
Preview panel (centre panel).

Hosts all preview sub-widgets and switches between them based on the
currently active section and property.  This panel is strictly read-only:
it never owns state, never receives focus, and only visualises the
effective (staged) values.
"""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QStackedWidget, QWidget

from .models.staged_settings import StagedSettings
from .preview.theme_preview import ThemePreview
from .preview.wallpaper_preview import WallpaperPreview
from .preview.font_preview import FontPreview
from .preview.accent_preview import AccentPreview
from .preview.placeholder_preview import PlaceholderPreview


class PreviewPanel(QWidget):
    """Centre preview panel that visualises staged settings."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Sub-preview widgets
        self._theme_preview = ThemePreview()
        self._wallpaper_preview = WallpaperPreview()
        self._font_preview = FontPreview()
        self._accent_preview = AccentPreview()

        # Placeholder previews for non-appearance sections
        self._placeholders: dict[str, PlaceholderPreview] = {}
        placeholder_sections = {
            "Wi-Fi": "\U0001f4f6",
            "Bluetooth": "\U0001f4e1",
            "Audio": "\U0001f50a",
            "Modules": "\U0001f4e6",
            "About": "\u2139\ufe0f",
        }
        for name, icon in placeholder_sections.items():
            ph = PlaceholderPreview()
            ph.set_section(name, icon)
            self._placeholders[name] = ph

        # Stacked widget for switching
        from PyQt6.QtWidgets import QVBoxLayout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self._stack = QStackedWidget()
        self._stack.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        layout.addWidget(self._stack)

        # Add widgets to stack
        self._stack.addWidget(self._theme_preview)       # 0
        self._stack.addWidget(self._wallpaper_preview)    # 1
        self._stack.addWidget(self._font_preview)         # 2
        self._stack.addWidget(self._accent_preview)       # 3
        for ph in self._placeholders.values():
            self._stack.addWidget(ph)

        self._current_section = "Appearance"
        self._current_property = "Theme"
        self._staged_settings: StagedSettings | None = None

        # Style
        self.setStyleSheet("background-color: #1a1b26;")

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #

    def set_staged_settings(self, staged: StagedSettings) -> None:
        self._staged_settings = staged
        staged.staged_changed.connect(self._on_staged_changed)
        staged.committed.connect(self._refresh_from_state)
        staged.discarded.connect(self._refresh_from_state)
        self._refresh_from_state()

    def set_section(self, section: str) -> None:
        self._current_section = section
        # Default to first property of section
        if section == "Appearance":
            self._current_property = "Theme"
        self._update_visible_preview()
        self._refresh_from_state()

    def set_property(self, section: str, prop: str) -> None:
        self._current_section = section
        self._current_property = prop
        self._update_visible_preview()
        self._refresh_from_state()

    # ------------------------------------------------------------------ #
    # Internal
    # ------------------------------------------------------------------ #

    def _update_visible_preview(self) -> None:
        """Switch the stacked widget to the appropriate preview."""
        if self._current_section != "Appearance":
            ph = self._placeholders.get(self._current_section)
            if ph:
                self._stack.setCurrentWidget(ph)
            return

        prop_widget_map = {
            "Theme": self._theme_preview,
            "Wallpaper": self._wallpaper_preview,
            "Font": self._font_preview,
            "Accent": self._accent_preview,
        }
        widget = prop_widget_map.get(self._current_property, self._theme_preview)
        self._stack.setCurrentWidget(widget)

    def _refresh_from_state(self) -> None:
        """Re-read effective values from staged settings and update previews."""
        if not self._staged_settings:
            return
        s = self._staged_settings
        self._theme_preview.set_theme(s.get_effective("Appearance", "Theme"))
        self._wallpaper_preview.set_wallpaper(s.get_effective("Appearance", "Wallpaper"))
        self._font_preview.set_font(s.get_effective("Appearance", "Font"))
        self._accent_preview.set_accent(s.get_effective("Appearance", "Accent"))

    def _on_staged_changed(self, section: str, prop: str, value: str) -> None:
        """React to a staged value change — update the relevant preview."""
        if section == "Appearance":
            dispatch = {
                "Theme": lambda v: self._theme_preview.set_theme(v),
                "Wallpaper": lambda v: self._wallpaper_preview.set_wallpaper(v),
                "Font": lambda v: self._font_preview.set_font(v),
                "Accent": lambda v: self._accent_preview.set_accent(v),
            }
            fn = dispatch.get(prop)
            if fn:
                fn(value)
