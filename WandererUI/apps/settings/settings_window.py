"""
Settings window — main application shell.

Assembles the three-panel layout (Navigation | Preview | Properties),
the Footer, and the Overlay.  Implements the focus state machine:

    Launch → Left Panel
          → Enter → Right Panel
                  → Enter → Overlay
                          → Esc/Confirm → Right Panel
                  → Esc → Left Panel
          → Esc → (confirm if staged) → Exit
"""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from .models.staged_settings import StagedSettings
from .navigation_panel import NavigationPanel
from .preview_panel import PreviewPanel
from .properties_panel import PropertiesPanel
from .overlay import Overlay
from .footer import Footer


class SettingsWindow(QMainWindow):
    """Standalone settings application window."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Settings")
        self.setMinimumSize(1000, 620)
        self.resize(1100, 700)

        # ---- State ---- #
        self._staged = StagedSettings(self)

        # ---- Panels ---- #
        self._nav_panel = NavigationPanel()
        self._preview_panel = PreviewPanel()
        self._props_panel = PropertiesPanel()
        self._footer = Footer()

        # Wire staged settings into panels
        self._props_panel.set_staged_settings(self._staged)
        self._preview_panel.set_staged_settings(self._staged)

        # ---- Layout ---- #
        central = QWidget()
        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        panels_layout = QHBoxLayout()
        panels_layout.setContentsMargins(0, 0, 0, 0)
        panels_layout.setSpacing(1)  # 1px gap as visual separator

        panels_layout.addWidget(self._nav_panel, 1)
        panels_layout.addWidget(self._preview_panel, 2)
        panels_layout.addWidget(self._props_panel, 1)

        root_layout.addLayout(panels_layout, 1)
        root_layout.addWidget(self._footer)

        self.setCentralWidget(central)

        # Overlay must be parented to the central widget so it floats
        # above the panels and covers the full content area.
        self._overlay = Overlay(central)
        self._overlay.setGeometry(central.rect())

        # ---- Connections ---- #
        self._connect_signals()

        # ---- Initial state ---- #
        self._init_focus_state()

        # ---- Window styling ---- #
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1b26;
            }
        """)

    # ================================================================== #
    # Signal wiring
    # ================================================================== #

    def _connect_signals(self) -> None:
        # Navigation panel
        self._nav_panel.section_changed.connect(self._on_section_changed)
        self._nav_panel.section_activated.connect(self._on_section_activated)

        # Properties panel
        self._props_panel.property_activated.connect(self._on_property_activated)
        self._props_panel.back_requested.connect(self._on_props_back)
        self._props_panel.property_changed.connect(self._on_property_highlight_changed)

        # Overlay
        self._overlay.value_selected.connect(self._on_overlay_value)
        self._overlay.overlay_closed.connect(self._on_overlay_closed)
        self._overlay.apply_requested.connect(self._on_apply)
        self._overlay.discard_requested.connect(self._on_discard)

        # Staged settings changes → refresh properties display
        self._staged.staged_changed.connect(lambda *_: self._props_panel.refresh())
        self._staged.committed.connect(self._props_panel.refresh)
        self._staged.discarded.connect(self._props_panel.refresh)

    # ================================================================== #
    # Focus state machine
    # ================================================================== #

    def _init_focus_state(self) -> None:
        """Set initial focus to the navigation panel."""
        section = self._nav_panel.get_current_section()
        self._props_panel.set_section(section)
        self._preview_panel.set_section(section)

        self._focus_nav()

    def _focus_nav(self) -> None:
        """Give focus to the navigation (left) panel."""
        self._nav_panel.set_focus_active(True)
        self._props_panel.set_focus_active(False)
        self._nav_panel.setFocus()
        self._footer.set_context("sections")

    def _focus_props(self) -> None:
        """Give focus to the properties (right) panel."""
        self._nav_panel.set_focus_active(False)
        self._props_panel.set_focus_active(True)
        self._props_panel.setFocus()
        self._footer.set_context("properties")

    def _focus_overlay(self) -> None:
        """Focus is now owned by the overlay."""
        self._nav_panel.set_focus_active(False)
        self._props_panel.set_focus_active(False)
        self._footer.set_context("overlay")

    # ================================================================== #
    # Slot handlers — Navigation panel
    # ================================================================== #

    def _on_section_changed(self, section: str) -> None:
        """Selection moved in the nav panel — update preview + props."""
        self._props_panel.set_section(section)
        self._preview_panel.set_section(section)

    def _on_section_activated(self, section: str) -> None:
        """Enter pressed in nav panel — drill into properties."""
        self._props_panel.set_section(section)
        self._preview_panel.set_section(section)
        self._focus_props()

    # ================================================================== #
    # Slot handlers — Properties panel
    # ================================================================== #

    def _on_property_activated(self, section: str, prop: str) -> None:
        """Enter pressed on a property — open the overlay."""
        current_value = self._staged.get_effective(section, prop)
        self._overlay.setGeometry(self.centralWidget().rect())
        self._overlay.open_for_property(section, prop, current_value)
        self._focus_overlay()

    def _on_props_back(self) -> None:
        """Esc pressed in properties — return to nav panel."""
        self._focus_nav()

    def _on_property_highlight_changed(self, section: str, prop: str) -> None:
        """Property selection moved — update preview to show relevant preview."""
        if section == "Appearance":
            self._preview_panel.set_property(section, prop)

    # ================================================================== #
    # Slot handlers — Overlay
    # ================================================================== #

    def _on_overlay_value(self, section: str, prop: str, value: str) -> None:
        """A value was selected/navigated in the overlay — stage it."""
        self._staged.stage(section, prop, value)

    def _on_overlay_closed(self) -> None:
        """Overlay dismissed — return focus to properties."""
        self._focus_props()

    def _on_apply(self) -> None:
        """Commit staged changes and exit."""
        self._staged.commit()
        self.close()

    def _on_discard(self) -> None:
        """Discard staged changes and exit."""
        self._staged.discard()
        self.close()

    # ================================================================== #
    # Esc from navigation = quit (with confirmation if staged)
    # ================================================================== #

    def keyPressEvent(self, event: QKeyEvent) -> None:  # noqa: N802
        """Catch Esc at the window level when nav panel has focus."""
        if event.key() == Qt.Key.Key_Escape and self._nav_panel.hasFocus():
            if self._staged.has_staged_changes():
                self._overlay.setGeometry(self.centralWidget().rect())
                self._overlay.open_confirm_discard()
                self._focus_overlay()
            else:
                self.close()
        else:
            super().keyPressEvent(event)

    # ================================================================== #
    # Resize handling — keep overlay sized to central widget
    # ================================================================== #

    def resizeEvent(self, event) -> None:  # noqa: N802
        super().resizeEvent(event)
        if self._overlay.isVisible():
            self._overlay.setGeometry(self.centralWidget().rect())
