from apps.settings.controller import SettingsController

from apps.settings.providers import (
    SystemInfoProvider
)

from apps.settings.ui.settings_window import (
    SettingsWindow
)


def create_settings_application(maaya):
    """
    Create and return a fully initialized
    Settings application.
    """

    controller = SettingsController()

    providers = {
        "system_info": SystemInfoProvider()
    }

    return SettingsWindow(
        controller,
        maaya,
        providers
    )