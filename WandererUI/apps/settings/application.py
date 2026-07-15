from apps.settings.controller import SettingsController

from apps.settings.providers import (
    SystemInfoProvider
)

from core.desktop_extension import DesktopApplication

class SettingsApplication(DesktopApplication):

    def __init__(self, maaya):

        self.maaya = maaya

        self.controller = SettingsController()

        self.providers = {
            "system_info": SystemInfoProvider()
        }

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

        return None

    def activate(self, item):
        """Activate the selected Settings category."""

        self.controller.set_current_page(
            item
        )

    def activate_property(
        self,
        property_name
    ):
        """Activate the selected property."""

        print(
            f"[Settings] {property_name}"
        )

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