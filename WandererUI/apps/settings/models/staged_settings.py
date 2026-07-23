"""
Staged settings state manager.

Maintains two layers of configuration values:
  - committed: the persisted/applied values
  - staged: in-flight edits not yet applied

The preview system reads *effective* values (staged if present, else committed).
Commit promotes staged → committed.  Discard drops staged entirely.
"""

from __future__ import annotations

from typing import Optional

from PyQt6.QtCore import QObject, pyqtSignal


class StagedSettings(QObject):
    """Manages committed and staged configuration values."""

    # (section, property, new_value)
    staged_changed = pyqtSignal(str, str, str)
    committed = pyqtSignal()
    discarded = pyqtSignal()

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

        # Key format: (section_name, property_name) → option name
        self._committed: dict[tuple[str, str], str] = {}
        self._staged: dict[tuple[str, str], str] = {}

        self._init_defaults()

    # --------------------------------------------------------------------- #
    # Default values
    # --------------------------------------------------------------------- #

    def _init_defaults(self) -> None:
        """Populate committed values with sensible defaults."""
        defaults: dict[tuple[str, str], str] = {
            ("Appearance", "Theme"): "Tokyo Night",
            ("Appearance", "Wallpaper"): "Midnight Gradient",
            ("Appearance", "Font"): "Inter",
            ("Appearance", "Accent"): "Blue",
            ("Wi-Fi", "Network"): "Home Network",
            ("Wi-Fi", "Status"): "Connected",
            ("Bluetooth", "Devices"): "Headphones",
            ("Bluetooth", "Status"): "On",
            ("Audio", "Output Device"): "Built-in Speakers",
            ("Audio", "Volume"): "75%",
            ("Modules", "Installed"): "3 Modules",
            ("Modules", "Available"): "12 Modules",
            ("About", "Version"): "1.0.0",
            ("About", "System"): "Linux x86_64",
        }
        self._committed.update(defaults)

    # --------------------------------------------------------------------- #
    # Read access
    # --------------------------------------------------------------------- #

    def get_committed(self, section: str, prop: str) -> str:
        """Return the committed value for *(section, prop)*."""
        return self._committed.get((section, prop), "")

    def get_staged(self, section: str, prop: str) -> Optional[str]:
        """Return the staged value if one exists, else ``None``."""
        return self._staged.get((section, prop))

    def get_effective(self, section: str, prop: str) -> str:
        """Return the staged value when present, otherwise the committed value."""
        staged = self._staged.get((section, prop))
        if staged is not None:
            return staged
        return self._committed.get((section, prop), "")

    # --------------------------------------------------------------------- #
    # Write access
    # --------------------------------------------------------------------- #

    def stage(self, section: str, prop: str, value: str) -> None:
        """Stage a new value.  If it matches the committed value, un-stage."""
        committed = self._committed.get((section, prop), "")
        if value == committed:
            # No real change – remove the staged entry if present.
            self._staged.pop((section, prop), None)
        else:
            self._staged[(section, prop)] = value
        self.staged_changed.emit(section, prop, value)

    def commit(self) -> None:
        """Promote all staged values to committed and clear the staging area."""
        self._committed.update(self._staged)
        self._staged.clear()
        self.committed.emit()

    def discard(self) -> None:
        """Drop all staged changes and revert to committed values."""
        self._staged.clear()
        self.discarded.emit()

    # --------------------------------------------------------------------- #
    # Query helpers
    # --------------------------------------------------------------------- #

    def has_staged_changes(self) -> bool:
        """Return ``True`` if any uncommitted staged changes exist."""
        return bool(self._staged)

    def get_all_staged(self) -> dict[tuple[str, str], str]:
        """Return a shallow copy of all staged values."""
        return dict(self._staged)

    def is_staged(self, section: str, prop: str) -> bool:
        """Return ``True`` if *(section, prop)* has a staged override."""
        return (section, prop) in self._staged
