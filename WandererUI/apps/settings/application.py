from core.desktop_extension import DesktopApplication

from apps.settings.models.state import SECTIONS
from apps.settings.models.staged_settings import StagedSettings
from apps.settings.models.state import SECTIONS, SECTION_REGISTRY
from apps.settings.preview.placeholder_preview import PlaceholderPreview
from apps.settings.preview_panel import PreviewPanel


class SettingsApplication(DesktopApplication):

    def __init__(
        self, 
        maaya,
        eidolon,
        nikola=None
    ):
        self.desktop = None

        self.maaya = maaya
        self.eidolon = eidolon
        self.nikola = nikola

        self.current_section = SECTIONS[0]

        self.current_property = None

        self.staged_settings = StagedSettings()

        self.initialize_appearance_state()

        self.preview_panel = PreviewPanel()
        self.preview_panel.set_staged_settings(
            self.staged_settings
        )

        self.placeholder_previews = {}

        placeholder_sections = {
            "Wi-Fi": "📶",
            "Bluetooth": "📡",
            "Audio": "🔊",
            "Modules": "📦",
            "About": "ℹ️",
        }

        for section, icon in placeholder_sections.items():
            preview = PlaceholderPreview()
            preview.set_section(section, icon)

            self.placeholder_previews[section] = preview

    def initialize_appearance_state(self):

        # Theme
        if self.maaya.theme is not None:
            theme = self.maaya.theme.__name__.split(".")[-1]

            self.staged_settings.set_committed(
                "Appearance",
                "Theme",
                theme
            )

        # Font
        if self.maaya.font is not None:
            font = self.maaya.font.get(
                "package",
                ""
            )

            self.staged_settings.set_committed(
                "Appearance",
                "Font",
                font
            )

        # Wallpaper
        if self.maaya.wallpaper is not None:
            wallpaper = self.maaya.wallpaper.get(
                "filename",
                ""
            )

            self.staged_settings.set_committed(
                "Appearance",
                "Wallpaper",
                wallpaper
            )

    def context_title(self) -> str:
        return self.current_section

    def set_desktop(self, desktop):
        self.desktop = desktop

    def name(self) -> str:
        return "Settings"

    def navigation_items(self) -> list[dict]:
        return [
            {
                "id": section.lower()
                    .replace(" ", "_")
                    .replace("-", "_"),
                "name": section,
            }
            for section in SECTIONS
        ]

    def context(self):

        section = SECTION_REGISTRY[self.current_section]

        if (
            self.current_section == "Wi-Fi"
            and self.nikola is not None
        ):

            enabled = self.nikola.wifi_enabled()

            network = (
                self.nikola.current_network()
                if enabled
                else None
            )

            return {
                "Wi-Fi": "On" if enabled else "Off",
                "Network": network or "Disconnected",
            }

        return {
            prop.name: self.staged_settings.get_effective(
                self.current_section,
                prop.name
            )
            for prop in section.properties
        }

    def viewport(self):

        if self.current_section == "Appearance":

            self.preview_panel.set_section(
                self.current_section
            )

            if self.current_property is not None:
                self.preview_panel.set_property(
                    self.current_section,
                    self.current_property
                )

            return self.preview_panel

        return self.placeholder_previews.get(
            self.current_section
        )

    def viewport_title(self) -> str:
        return "Preview"

    def footer_hints(self) -> str:
        return "↑↓ Navigate    ENTER Select    ESC Back"

    def on_enter(self) -> None:
        pass

    def request_exit(self) -> bool:

        if not self.staged_settings.has_staged_changes():
            return True

        self.desktop.show_overlay(
            "UNAPPLIED CHANGES",
            [
                {"name": "Apply"},
                {"name": "Discard"},
                {"name": "Cancel"},
            ],
            self.exit_option_selected
        )

        return False

    def exit_option_selected(self, value):

        if isinstance(value, dict):
            choice = value["name"]
        else:
            choice = value

        if choice == "Cancel":
            return

        if choice == "Discard":
            self.staged_settings.discard()
            self.desktop.exit_application()
            return

        if choice == "Apply":
            self.apply_changes()

    def apply_changes(self):

        changes = self.staged_settings.get_all_staged()

        for (section, prop), value in changes.items():

            if section != "Appearance":
                continue

            if prop == "Theme":

                self.maaya.load_theme(value)
                self.desktop.refresh("theme")

                self.eidolon.set(
                    "appearance",
                    "theme",
                    value
                )

            elif prop == "Font":

                self.maaya.load_font(value)
                self.desktop.refresh("font")

                self.eidolon.set(
                    "appearance",
                    "font",
                    value
                )

            elif prop == "Wallpaper":

                self.maaya.load_wallpaper(
                    "static",
                    value
                )
                self.desktop.refresh("wallpaper")

                self.eidolon.set(
                    "appearance",
                    "wallpaper",
                    {
                        "category": "static",
                        "filename": value
                    }
                )

        if not self.eidolon.save():
            print(
                "[Settings] Failed to persist "
                "state through Eidolon."
            )
            return

        self.staged_settings.commit()

        self.desktop.exit_application()

    def on_leave(self) -> None:
        pass

    def selection_changed(self, item):
        self.current_section = item["name"]

    def activate(self, item):
        self.current_section = item["name"]

        if self.desktop is not None:
            self.desktop.kaizen.set_focus("context")

    def appearance_options(self, property_name):

        if property_name == "Theme":
            return [
                {"name": theme}
                for theme in self.maaya.available_themes()
            ]

        if property_name == "Font":
            return [
                {"name": font}
                for font in self.maaya.available_fonts()
            ]

        if property_name == "Wallpaper":
            return [
                {"name": wallpaper}
                for wallpaper in self.maaya.available_wallpapers()
            ]

        return []

    def wifi_options(self, property_name):

        if self.nikola is None:
            return []

        if property_name == "Wi-Fi":
            return [
                {"name": "On"},
                {"name": "Off"},
            ]

        if property_name == "Network":

            if not self.nikola.wifi_enabled():
                return [
                    {"name": "Wi-Fi is Off"}
                ]

            networks = self.nikola.available_networks()

            options = []

            for network in networks:

                ssid = network["ssid"]
                strength = network["strength"]
                secured = network["secured"]
                connected = network["connected"]

                marker = "●" if connected else " "

                security = "🔒" if secured else ""

                options.append({
                   "name": (
                        f"{marker} {ssid}    "
                        f"{strength}% {security}"
                    ),
                    "ssid": ssid,
                    "strength": strength,
                    "secured": secured,
                    "connected": connected,
                })

            if not options:
                return [
                    {"name": "No Networks Found"}
                ]

            return options

        return []
    def activate_property(self, property_name):

        section = SECTION_REGISTRY[self.current_section]

        prop = next(
            (
                prop
                for prop in section.properties
                if prop.name == property_name
            ),
            None
        )

        if prop is None:
            return

        if self.current_section == "Appearance":

            options = self.appearance_options(
                property_name
            )

        elif self.current_section == "Wi-Fi":

            options = self.wifi_options(
                property_name
            )

        else:

            options = prop.options

        if not options:
            return

        self.current_property = property_name

        self.desktop.show_overlay(
            property_name.upper(),
            options,
            self.option_selected
        )

    def option_selected(self, value):

        if self.current_property is None:
            return

        if isinstance(value, dict):
            selected_value = value["name"]
        else:
            selected_value = value

        if self.current_section == "Wi-Fi":

            if self.nikola is None:
                return

            if self.current_property == "Wi-Fi":

                enabled = selected_value == "On"

                if not self.nikola.set_wifi_enabled(enabled):
                    print(
                        "[Settings] Failed to change "
                        "Wi-Fi state."
                    )
                    return

                if self.desktop is not None:
                    self.desktop.refresh_application()

                return
            
            if self.current_property == "Network":

                if not isinstance(value, dict):
                    return

                ssid = value.get("ssid")

                if not ssid:
                    return

                # Already connected.
                if value.get("connected"):
                    return

                saved = self.nikola.saved_network(
                    ssid
                )

                if saved is not None:

                    if not self.nikola.connect_saved_network(
                        ssid
                    ):
                        print(
                            "[Settings] Failed to connect "
                            "to saved network:",
                            repr(ssid)
                        )
                        return

                    if self.desktop is not None:
                        self.desktop.refresh_application()

                    return

                print(
                    "[Settings] Network requires "
                    "new connection:",
                    repr(ssid)
                )

                return

        self.staged_settings.stage(
            self.current_section,
            self.current_property,
            selected_value
        )

        if self.desktop is not None:
            self.desktop.refresh_application()

def create_application(
    maaya,
    eidolon,
    services=None
):

    services = services or {}

    return SettingsApplication(
        maaya,
        eidolon,
        nikola=services.get("nikola")
    )