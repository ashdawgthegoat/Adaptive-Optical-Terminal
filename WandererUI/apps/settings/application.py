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

        return None

    def viewport(self):

        return None

    def activate(self, item):
        """Activate the selected Settings category."""

        print(f"[Settings] {item}")

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