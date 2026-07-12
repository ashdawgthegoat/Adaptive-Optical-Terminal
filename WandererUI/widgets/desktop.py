from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt6.QtCore import QTimer

from widgets.header import Header
from widgets.footer import Footer
from widgets.navigation_panel import NavigationPanel
from widgets.viewport import Viewport
from widgets.context_panel import ContextPanel
from utils.system_info import SystemInfo


class Desktop(QWidget):

    def __init__(
        self,
        maaya,
        animus,
        kaizen
    ):

        super().__init__()

        self.maaya = maaya

        self.animus = animus

        self.kaizen = kaizen

        self.workspace = None

        self.workspace_active = False

        self.header = Header(
            self.maaya
        )

        self.navigation = NavigationPanel(
            self.maaya
        )

        self.viewport = Viewport(
            self.maaya
        )

        self.context = ContextPanel(
            self.maaya
        )

        self.footer = Footer(
            self.maaya
        )

        self.build_ui()

        self.set_navigation_items(
            self.animus.list_applications()
        )

        self.viewport.show_wallpaper()

        self.update_system_context()

        self.kaizen.focus_changed.connect(
            self.update_focus
        )

        self.context_timer = QTimer(self)

        self.context_timer.timeout.connect(
            self.update_system_context
        )

        self.context_timer.start(1000)

    def build_ui(self):

        spacing = self.maaya.theme.Spacing

        desktop_layout = QVBoxLayout()

        desktop_layout.setContentsMargins(
            spacing.OUTER_MARGIN,
            spacing.OUTER_MARGIN,
            spacing.OUTER_MARGIN,
            spacing.OUTER_MARGIN
        )

        desktop_layout.setSpacing(
            spacing.SECTION_SPACING
        )

        body_layout = QHBoxLayout()

        body_layout.setSpacing(4)

        body_layout.setContentsMargins(
            spacing.INNER_MARGIN,
            0,
            spacing.INNER_MARGIN,
            0
        )

        header_layout = QHBoxLayout()

        header_layout.setContentsMargins(
            spacing.INNER_MARGIN,
            0,
            spacing.INNER_MARGIN,
            0
        )

        header_layout.addWidget(
            self.header
        )

        desktop_layout.addLayout(
            header_layout
        )

        body_layout.addWidget(
            self.navigation,
            2
        )

        body_layout.addWidget(
            self.viewport,
            6
        )

        body_layout.addWidget(
            self.context,
            2
        )

        desktop_layout.addLayout(
            body_layout,
            stretch=1
        )

        footer_layout = QHBoxLayout()

        footer_layout.setContentsMargins(
            spacing.INNER_MARGIN,
            0,
            spacing.INNER_MARGIN,
            0
        )

        footer_layout.addWidget(
            self.footer
        )

        desktop_layout.addLayout(
            footer_layout
        )

        self.setLayout(
            desktop_layout
        )

    def current_panel(self):

        panels = {

            "header": self.header,
            "navigation": self.navigation,
            "viewport": self.viewport,
            "context": self.context,
            "footer": self.footer,

        }

        return panels[self.kaizen.current()]

    def update_focus(self, region):

        self.header.set_inactive()
        self.navigation.set_inactive()
        self.viewport.set_inactive()
        self.context.set_inactive()
        self.footer.set_inactive()

        match region:

            case "header":
                self.header.set_active()

            case "navigation":
                self.navigation.set_active()

            case "viewport":
                self.viewport.set_active()

            case "context":
                self.context.set_active()

            case "footer":
                self.footer.set_active()

    def update_system_context(self):

        self.context.set_context({

            "CPU": SystemInfo.cpu(),

            "Memory": SystemInfo.memory(),

            "Storage": SystemInfo.storage(),

            "Battery": SystemInfo.battery(),

            "Hostname": SystemInfo.hostname(),

            "Status": SystemInfo.status(),

        })

    # ==========================================================
    # Workspace Management
    # ==========================================================

    def enter_workspace(self):
        """Enter workspace mode."""
        self.workspace_active = True


    def exit_workspace(self):
        """Return to desktop mode."""
        self.workspace_active = False
        self.workspace = None


    def set_workspace(self, workspace):
        """Set the currently hosted workspace."""
        self.workspace = workspace


    def current_workspace(self):
        """Return the active workspace."""
        return self.workspace


    def in_workspace(self):
        """True if a workspace is active."""
        return self.workspace_active


    def set_navigation_items(self, items):
        """Replace navigation items."""
        self.navigation.set_items(items)