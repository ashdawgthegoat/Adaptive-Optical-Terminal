"""
Settings data model definitions.

Defines the structure of sections, properties, and their available options.
This is the single source of truth for what the settings application displays.
"""

from dataclasses import dataclass, field


@dataclass
class PropertyInfo:
    """A single editable property within a section."""
    name: str
    options: list[dict[str, str]] = field(default_factory=list)


@dataclass
class SectionInfo:
    """A navigable section in the settings application."""
    name: str
    icon: str
    properties: list[PropertyInfo] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Section and property definitions
# ---------------------------------------------------------------------------

_APPEARANCE = SectionInfo(
    name="Appearance",
    icon="\U0001f3a8",  # 🎨
    properties=[
        PropertyInfo(
            name="Theme",
        ),
        PropertyInfo(
            name="Wallpaper",
        ),
        PropertyInfo(
            name="Font",
        ),
    ],
)

_WIFI = SectionInfo(
    name="Wi-Fi",
    icon="\U0001f4f6",  # 📶
    properties=[
        PropertyInfo(
            name="Wi-Fi",
        ),
        PropertyInfo(
            name="Network",
        ),
    ],
)

_BLUETOOTH = SectionInfo(
    name="Bluetooth",
    icon="\U0001f4e1",  # 📡
    properties=[
        PropertyInfo(
            name="Devices",
            options=[
                {"name": "Headphones"},
                {"name": "Keyboard"},
                {"name": "Mouse"},
                {"name": "Speaker"},
            ],
        ),
        PropertyInfo(
            name="Status",
            options=[
                {"name": "On"},
                {"name": "Off"},
            ],
        ),
    ],
)

_AUDIO = SectionInfo(
    name="Audio",
    icon="\U0001f50a",  # 🔊
    properties=[
        PropertyInfo(
            name="Output Device",
            options=[
                {"name": "Built-in Speakers"},
                {"name": "HDMI Output"},
                {"name": "USB Audio"},
                {"name": "Bluetooth Speaker"},
            ],
        ),
        PropertyInfo(
            name="Volume",
            options=[
                {"name": "25%"},
                {"name": "50%"},
                {"name": "75%"},
                {"name": "100%"},
            ],
        ),
    ],
)

_MODULES = SectionInfo(
    name="Modules",
    icon="\U0001f4e6",  # 📦
    properties=[
        PropertyInfo(
            name="Installed",
            options=[
                {"name": "3 Modules"},
                {"name": "5 Modules"},
                {"name": "8 Modules"},
            ],
        ),
        PropertyInfo(
            name="Available",
            options=[
                {"name": "12 Modules"},
                {"name": "15 Modules"},
                {"name": "20 Modules"},
            ],
        ),
    ],
)

_ABOUT = SectionInfo(
    name="About",
    icon="\u2139\ufe0f",  # ℹ️
    properties=[
        PropertyInfo(
            name="Version",
            options=[
                {"name": "1.0.0"},
                {"name": "1.1.0-beta"},
            ],
        ),
        PropertyInfo(
            name="System",
            options=[
                {"name": "Linux x86_64"},
                {"name": "Linux aarch64"},
            ],
        ),
    ],
)

# Ordered list of section names (determines display order).
SECTIONS: list[str] = [
    "Appearance",
    "Wi-Fi",
    "Bluetooth",
    "Audio",
    "Modules",
    "About",
]

# Lookup table: section name → SectionInfo.
SECTION_REGISTRY: dict[str, SectionInfo] = {
    s.name: s
    for s in [_APPEARANCE, _WIFI, _BLUETOOTH, _AUDIO, _MODULES, _ABOUT]
}
