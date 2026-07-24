from core.desktop_extension import DesktopApplication

from apps.settings.models.state import SECTIONS
from apps.settings.models.staged_settings import StagedSettings
from apps.settings.models.state import SECTIONS, SECTION_REGISTRY
from apps.settings.preview.theme_preview import ThemePreview
from apps.settings.preview.placeholder_preview import PlaceholderPreview


class SettingsApplication(DesktopApplication):

    def __init__(self):
        self.desktop = None

        self.current_section = SECTIONS[0]

        self.staged_settings = StagedSettings()

        self.theme_preview = ThemePreview()

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

        return {
            prop.name: self.staged_settings.get_effective(
                self.current_section,
                prop.name
            )
            for prop in section.properties
        }

    def viewport(self):

        if self.current_section == "Appearance":

            self.theme_preview.set_theme(
                self.staged_settings.get_effective(
                    "Appearance",
                    "Theme"
                )
            )

            return self.theme_preview

        return self.placeholder_previews.get(
            self.current_section
        )

    def viewport_title(self) -> str:
        return "Preview"

    def footer_hints(self) -> str:
        return "↑↓ Navigate    ENTER Select    ESC Back"

    def on_enter(self) -> None:
        pass

    def on_leave(self) -> None:
        pass

    def selection_changed(self, item):
        self.current_section = item["name"]

    def activate(self, item):
        self.current_section = item["name"]

        if self.desktop is not None:
            self.desktop.kaizen.set_focus("context")

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

        if prop is None or not prop.options:
            return

        self.desktop.show_overlay(
            property_name.upper(),
            prop.options,
            self.option_selected
        )

    def option_selected(self, value):

        print(
            f"[Settings] selected option: {value}"
        )

def create_application(maaya):
    return SettingsApplication()