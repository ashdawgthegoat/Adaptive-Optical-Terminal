# =============================================================================
# Settings Application — Appearance Page
# =============================================================================
#
# Single page with three collapsible sections: Themes, Wallpapers, Fonts.
# Unified keyboard navigation through a virtual flat list of all navigable
# items (section headers + option items within expanded sections).
#
# =============================================================================

import sys
from pathlib import Path
from enum import Enum, auto

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QFrame
from PyQt6.QtCore import Qt

from .base_page import BasePage
from ..theme import Palette
from ..widgets.option_list import OptionList
from ..widgets.collapsible_section import CollapsibleSection


# =============================================================================
# Navigation Item Types
# =============================================================================

class _NavKind(Enum):
    """Kind of item in the virtual navigation list."""
    HEADER = auto()
    OPTION = auto()


# =============================================================================
# AppearancePage
# =============================================================================

class AppearancePage(BasePage):
    """Appearance settings: Themes, Wallpapers, and Fonts.

    Three collapsible sections, each containing an OptionList.
    Keyboard navigation moves through a unified virtual list of
    section headers and option items.
    """

    # =========================================================================
    # Construction
    # =========================================================================

    def __init__(
        self,
        controller,
        theme_provider,
        wallpaper_provider,
        font_provider,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self._controller = controller
        self._theme_provider = theme_provider
        self._wallpaper_provider = wallpaper_provider
        self._font_provider = font_provider

        # Virtual navigation index
        self._nav_index = 0

        self._build_ui()

    # =========================================================================
    # BasePage Overrides
    # =========================================================================

    def page_title(self) -> str:
        return "Appearance"

    def hint_text(self) -> str:
        return "↑↓ Navigate   Enter Apply   ←→ Collapse/Expand   Esc Back"

    def on_enter(self) -> None:
        """Refresh all three lists from providers."""
        self._refresh_themes()
        self._refresh_wallpapers()
        self._refresh_fonts()
        self._rebuild_nav()
        self._nav_index = 0
        self._apply_nav_highlight()

    def on_leave(self) -> None:
        """Clean up focus state when leaving the page."""
        pass

    # =========================================================================
    # Keyboard Navigation
    # =========================================================================

    def keyPressEvent(self, event) -> None:
        """Handle unified keyboard navigation through the virtual list."""
        key = event.key()
        nav = self._nav_items

        if not nav:
            super().keyPressEvent(event)
            return

        if key in (Qt.Key.Key_Up, Qt.Key.Key_K):
            if self._nav_index > 0:
                self._nav_index -= 1
                self._apply_nav_highlight()

        elif key in (Qt.Key.Key_Down, Qt.Key.Key_J):
            if self._nav_index < len(nav) - 1:
                self._nav_index += 1
                self._apply_nav_highlight()

        elif key == Qt.Key.Key_Home:
            self._nav_index = 0
            self._apply_nav_highlight()

        elif key == Qt.Key.Key_End:
            self._nav_index = len(nav) - 1
            self._apply_nav_highlight()

        elif key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self._activate_current()

        elif key == Qt.Key.Key_Left:
            self._collapse_current()

        elif key == Qt.Key.Key_Right:
            self._expand_current()

        else:
            super().keyPressEvent(event)

    # =========================================================================
    # Internal — UI Construction
    # =========================================================================

    def _build_ui(self) -> None:
        """Build the scroll area with three collapsible sections."""
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)

        # --- Scroll area ---
        self._scroll = QScrollArea(self)
        self._scroll.setWidgetResizable(True)
        self._scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self._scroll.setFrameShape(QFrame.Shape.NoFrame)

        content = QWidget()
        self._content_layout = QVBoxLayout(content)
        self._content_layout.setContentsMargins(16, 16, 16, 16)
        self._content_layout.setSpacing(12)

        # --- Themes section ---
        self._theme_section = CollapsibleSection("Themes", content)
        self._theme_list = OptionList()
        self._theme_section.set_content(self._theme_list)
        self._theme_list.item_activated.connect(self._on_theme_activated)
        self._theme_section.toggled.connect(lambda _: self._on_section_toggled())
        self._content_layout.addWidget(self._theme_section)

        # --- Wallpapers section ---
        self._wallpaper_section = CollapsibleSection("Wallpapers", content)
        self._wallpaper_list = OptionList()
        self._wallpaper_section.set_content(self._wallpaper_list)
        self._wallpaper_list.item_activated.connect(self._on_wallpaper_activated)
        self._wallpaper_section.toggled.connect(lambda _: self._on_section_toggled())
        self._content_layout.addWidget(self._wallpaper_section)

        # --- Fonts section ---
        self._font_section = CollapsibleSection("Fonts", content)
        self._font_list = OptionList()
        self._font_section.set_content(self._font_list)
        self._font_list.item_activated.connect(self._on_font_activated)
        self._font_section.toggled.connect(lambda _: self._on_section_toggled())
        self._content_layout.addWidget(self._font_section)

        self._content_layout.addStretch()

        self._scroll.setWidget(content)
        outer_layout.addWidget(self._scroll)

        # Section registry: (section_widget, option_list, apply_callback)
        self._sections = [
            (self._theme_section, self._theme_list, self._on_theme_activated),
            (self._wallpaper_section, self._wallpaper_list, self._on_wallpaper_activated),
            (self._font_section, self._font_list, self._on_font_activated),
        ]

        # Virtual nav list — rebuilt when sections expand/collapse
        self._nav_items: list[tuple[_NavKind, int, int]] = []
        # Each entry: (kind, section_index, item_index_within_section)
        # For HEADER: item_index is -1

    # =========================================================================
    # Internal — Data Refresh
    # =========================================================================

    def _refresh_themes(self) -> None:
        """Reload themes from the provider."""
        themes = self._theme_provider.list_themes()
        names = [t.name for t in themes]
        active = self._controller.active_theme
        self._theme_list.set_items(names, active)

    def _refresh_wallpapers(self) -> None:
        """Reload wallpapers from the provider."""
        wallpapers = self._wallpaper_provider.list_wallpapers()
        names = [w.name for w in wallpapers]
        active = self._controller.active_wallpaper
        self._wallpaper_list.set_items(names, active)

    def _refresh_fonts(self) -> None:
        """Reload fonts from the provider."""
        fonts = self._font_provider.list_fonts()
        families = [f.family for f in fonts]
        active = self._controller.active_font
        self._font_list.set_items(families, active)

    # =========================================================================
    # Internal — Virtual Navigation List
    # =========================================================================

    def _rebuild_nav(self) -> None:
        """Rebuild the flat virtual navigation list from current section state."""
        self._nav_items = []

        for sec_idx, (section, option_list, _callback) in enumerate(self._sections):
            # Section header is always navigable
            self._nav_items.append((_NavKind.HEADER, sec_idx, -1))

            # If expanded, add each item
            if section.is_expanded():
                for item_idx in range(option_list.item_count()):
                    self._nav_items.append((_NavKind.OPTION, sec_idx, item_idx))

    def _on_section_toggled(self) -> None:
        """Handle a section being expanded or collapsed."""
        # Remember what we were on
        old_item = self._nav_items[self._nav_index] if self._nav_items else None

        self._rebuild_nav()

        # Try to stay on the same logical item
        if old_item is not None:
            # If it was a header, find that header
            if old_item[0] == _NavKind.HEADER:
                for i, item in enumerate(self._nav_items):
                    if item[0] == _NavKind.HEADER and item[1] == old_item[1]:
                        self._nav_index = i
                        break
            else:
                # Clamp
                self._nav_index = min(self._nav_index, len(self._nav_items) - 1)

        self._nav_index = max(0, min(self._nav_index, len(self._nav_items) - 1))
        self._apply_nav_highlight()

    def _apply_nav_highlight(self) -> None:
        """Update visual state to reflect the current nav_index position."""
        if not self._nav_items:
            return

        kind, sec_idx, item_idx = self._nav_items[self._nav_index]

        # Clear all option list selections first
        for _section, option_list, _cb in self._sections:
            option_list.set_selected_index(-1)

        # Clear all header highlights
        for section, _ol, _cb in self._sections:
            section._header.setStyleSheet(
                f"color: {Palette.SECONDARY};"
                f" font-family: 'Departure Mono Nerd Font';"
                f" font-size: 13px;"
                f" padding: 8px 4px;"
                f" border-bottom: 1px solid {Palette.SEPARATOR};"
                f" background-color: transparent;"
            )

        if kind == _NavKind.HEADER:
            # Highlight the section header
            section = self._sections[sec_idx][0]
            section._header.setStyleSheet(
                f"color: {Palette.PRIMARY};"
                f" font-family: 'Departure Mono Nerd Font';"
                f" font-size: 13px;"
                f" padding: 8px 4px;"
                f" border-bottom: 1px solid {Palette.SEPARATOR};"
                f" border-left: 3px solid {Palette.ACCENT};"
                f" background-color: {Palette.SURFACE_SELECTED};"
            )
            # Ensure header is visible
            self._scroll.ensureWidgetVisible(section._header, 0, 50)

        elif kind == _NavKind.OPTION:
            # Select the item in the appropriate option list
            option_list = self._sections[sec_idx][1]
            option_list.set_selected_index(item_idx)

    # =========================================================================
    # Internal — Actions
    # =========================================================================

    def _activate_current(self) -> None:
        """Activate the currently navigated item (Enter key)."""
        if not self._nav_items:
            return

        kind, sec_idx, item_idx = self._nav_items[self._nav_index]

        if kind == _NavKind.HEADER:
            # Toggle the section
            section = self._sections[sec_idx][0]
            section.toggle()

        elif kind == _NavKind.OPTION:
            # Apply the selected option
            option_list = self._sections[sec_idx][1]
            item = option_list.selected_item()
            if item is not None:
                callback = self._sections[sec_idx][2]
                callback(item)

    def _collapse_current(self) -> None:
        """Collapse the section at the current position (Left arrow)."""
        if not self._nav_items:
            return

        kind, sec_idx, _item_idx = self._nav_items[self._nav_index]

        section = self._sections[sec_idx][0]
        if section.is_expanded():
            section.collapse()

            # Move nav to the section header
            for i, item in enumerate(self._nav_items):
                if item[0] == _NavKind.HEADER and item[1] == sec_idx:
                    self._nav_index = i
                    break

    def _expand_current(self) -> None:
        """Expand the section at the current position (Right arrow)."""
        if not self._nav_items:
            return

        kind, sec_idx, _item_idx = self._nav_items[self._nav_index]

        section = self._sections[sec_idx][0]
        if not section.is_expanded():
            section.expand()

    # =========================================================================
    # Internal — Activation Callbacks
    # =========================================================================

    def _on_theme_activated(self, name: str) -> None:
        """Apply the selected theme."""
        self._controller.set_active_theme(name)
        self._refresh_themes()
        self._rebuild_nav()
        self._apply_nav_highlight()

    def _on_wallpaper_activated(self, name: str) -> None:
        """Apply the selected wallpaper."""
        self._controller.set_active_wallpaper(name)
        self._refresh_wallpapers()
        self._rebuild_nav()
        self._apply_nav_highlight()

    def _on_font_activated(self, family: str) -> None:
        """Apply the selected font."""
        self._controller.set_active_font(family)
        self._refresh_fonts()
        self._rebuild_nav()
        self._apply_nav_highlight()


# =============================================================================
# Standalone Entry Point
# =============================================================================

if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[4]
    sys.path.insert(0, str(project_root))

    from PyQt6.QtWidgets import QApplication
    from apps.settings.ui.theme import load_font, build_stylesheet
    from apps.settings.providers import ThemeProvider, WallpaperProvider, FontProvider
    from apps.settings.controller import SettingsController

    assets = project_root / "assets"

    app = QApplication(sys.argv)
    load_font(str(assets / "fonts" / "system" / "DepartureMonoNerdFont-Regular.otf"))
    app.setStyleSheet(build_stylesheet())

    controller = SettingsController()
    page = AppearancePage(
        controller,
        ThemeProvider(str(assets / "themes")),
        WallpaperProvider(str(assets / "wallpapers")),
        FontProvider(str(assets / "fonts")),
    )
    page.on_enter()
    page.setMinimumSize(600, 400)
    page.show()
    sys.exit(app.exec())
