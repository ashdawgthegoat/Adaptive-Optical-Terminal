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
from widgets.overlay import Overlay


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

        self.application = None

        self.application_active = False

        self.overlay_callback = None

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

        self.overlay = Overlay()

        self.build_ui()

        self.set_navigation_items(
            self.animus.list_applications()
        )

        self.viewport.show_wallpaper()

        self.update_system_context()

        self.kaizen.focus_changed.connect(
            self.update_focus
        )

        self.animus.applications_changed.connect(
            self.refresh_navigation
        )

        self.navigation.activated.connect(
            self.activate_navigation_item
        )

        self.overlay.item_selected.connect(
            self.overlay_selected
        )

        self.overlay.cancelled.connect(
            self.hide_overlay
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

        desktop_layout.addWidget(
            self.overlay
        )

    def activate_navigation_item(self, item):
        """Handle activation from the Navigation Panel."""

        if not self.in_application():

            self.animus.launch(
                item["id"]
            )

            return

        self.application.activate(
            item
        )

        self.refresh_application()

    def activate_context_item(self):
        """Handle activation from the Context Panel."""

        if not self.in_application():
            return

        property_name = self.context.activate()

        if property_name is None:
            return

        self.application.activate_property(
            property_name
        )

    def refresh_navigation(self):
        """Refresh the Navigation Panel."""

        self.set_navigation_items(
            self.animus.list_applications()
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

        if self.in_application():
            return

        self.context.set_context({

            "CPU": SystemInfo.cpu(),

            "Memory": SystemInfo.memory(),

            "Storage": SystemInfo.storage(),

            "Battery": SystemInfo.battery(),

            "Hostname": SystemInfo.hostname(),

            "Status": SystemInfo.status(),

        })

    # ==========================================================
    # Desktop Application Management
    # ==========================================================

    def enter_application(self, application):
        """Host a Desktop Application."""

        print("[4] enter_application()")

        self.application = application
        self.application.set_desktop(
            self
        )
        self.application_active = True
        self.context_timer.stop()

        # Navigation

        self.navigation.set_title(
            application.name().upper()
        )

        self.viewport.set_title(
            application.viewport_title()
        )

        self.navigation.set_items(
            application.navigation_items()
        )

        self.refresh_application()

        application.on_enter()

    def refresh_application(self):
        """Refresh the hosted Desktop Application."""

        if self.application is None:
            return

        # Footer

        self.footer.set_controls(
            self.application.footer_hints()
        )

        # Context

        context = self.application.context()

        if context is not None:

            self.context.set_title(
                self.application.controller.current_page.upper()
            )

            self.context.set_properties(
                context
            )

        # Viewport

        self.viewport.set_title(
            self.application.viewport_title()
        )

        preview = self.application.viewport()

        if preview is not None:

            self.viewport.show_preview(
                preview
            )

    def exit_application(self):
        """Return to the normal desktop."""

        if self.application is not None:
            self.application.on_leave()

        self.application = None
        self.application_active = False

        self.viewport.set_title(
            "Viewport"
        )

        self.navigation.set_title(
            "Applications"
        )

        self.context_timer.start(1000)


    def current_application(self):
        """Return the active Desktop Application."""

        return self.application


    def in_application(self):
        """True if a Desktop Application is active."""

        return self.application_active


    def set_navigation_items(self, items):
        """Replace navigation items."""
        self.navigation.set_items(items)

    def refresh(
        self,
        target
    ):

        match target:

            case "theme":

                self.header.refresh_presentation()

                self.navigation.refresh_presentation()

                self.viewport.refresh_presentation()

                self.context.refresh_presentation()

                self.footer.refresh_presentation()

                self.overlay.refresh_presentation()

            case "font":

                self.header.refresh_presentation()

                self.navigation.refresh_presentation()

                self.viewport.refresh_presentation()

                self.context.refresh_presentation()

                self.footer.refresh_presentation()

                self.overlay.refresh_presentation()

            case "wallpaper":

                self.viewport.show_wallpaper()

        if self.in_application():

            self.refresh_application()

        else:

            self.update_system_context()

        self.update()


    def show_overlay(
        self,
        title,
        items,
        callback
    ):

        self.overlay_callback = callback

        self.overlay.show_overlay(
            title,
            items
        )

    def hide_overlay(self):

        self.overlay.hide_overlay()

    def overlay_selected(self, item):
        """Forward overlay selection to the requester."""

        if self.overlay_callback is None:
            return

        self.overlay_callback(
            item
        )

        self.overlay_callback = None


    def overlay_visible(self):

        return self.overlay.isVisible()