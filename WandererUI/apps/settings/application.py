from apps.settings.controller import SettingsController

from apps.settings.providers import (
    SystemInfoProvider
)

from core.desktop_extension import DesktopApplication
from apps.settings.viewport import (
    SettingsViewport
)

class SettingsApplication(DesktopApplication):

    def __init__(self, maaya):

        self.maaya = maaya

        self.controller = SettingsController()

        self.providers = {
            "system_info": SystemInfoProvider()
        }

        self.viewport_widget = SettingsViewport(
            self.maaya
        )

        self.desktop = None

    def name(self):

        return "Settings"

    def navigation_items(self):

        return [
            "Appearance",
            "Wi-Fi",
            "Bluetooth",
            "Audio",
            "Modules",
            "About"
        ]

    def set_desktop(
        self,
        desktop
    ):

        self.desktop = desktop

    def context(self):

        match self.controller.current_page:

            case "Appearance":

                return {

                    "Theme": {
                        "value": self.maaya.theme.__name__,
                        "text": "Current theme"
                    },

                    "Wallpaper": {
                        "value": self.maaya.wallpaper["filename"],
                        "text": "Desktop wallpaper"
                    },

                    "Font": {
                        "value": self.maaya.font["package"],
                        "text": self.maaya.font["family"]
                    },

                    "Accent": {
                        "value": self.maaya.theme.Palette.ACCENT,
                        "text": "Accent colour"
                    }

                }

            case _:

                return {

                    "Status": "Coming Soon"

                }

    def viewport(self):

        return self.viewport_widget

    def activate(self, item):
        """Activate the selected Settings category."""

        self.controller.set_current_page(
            item
        )

        self.viewport_widget.show_page(
            item
        )

        self.desktop.refresh_application()

    def activate_property(
        self,
        property_name
    ):

        match property_name:

            case "Theme":

                self.desktop.show_overlay(
                    "Theme",
                    self.maaya.available_themes(),
                    self.theme_selected
                )

            case "Wallpaper":

                self.desktop.show_overlay(
                    "Wallpaper",
                    self.maaya.available_wallpapers(
                        "static"
                    ),
                    self.wallpaper_selected
                )

            case "Font":

                self.desktop.show_overlay(
                    "Font",
                    self.maaya.available_fonts(),
                    self.font_selected
                )

    def theme_selected(
        self,
        theme
    ):

        self.viewport_widget.preview_theme(
            theme
        )

        self.desktop.refresh_application()


    def wallpaper_selected(
        self,
        wallpaper
    ):

        wallpaper = self.maaya.load_wallpaper(
            "static",
            wallpaper
        )

        if wallpaper is None:
            return

        self.viewport_widget.preview_wallpaper(
            wallpaper
        )

        self.desktop.refresh_application()

    def font_selected(
        self,
        font
    ):

        self.viewport_widget.preview_font(
            font
        )

        self.desktop.refresh_application()

    def footer_hints(self):

        return (
            "↑↓ Navigate    "
            "ENTER Select    "
            "ESC Desktop"
        )

def create_settings_application(maaya):
    """
    Create and return a fully initialized
    Settings application.
    """

    return SettingsApplication(
        maaya
    )