import json
from pathlib import Path
from typing import Any


class Eidolon:
    """
    Persistent system-state service for WandererUI.

    Eidolon remembers configuration and state across UI sessions.
    It does not apply that state itself; other services remain
    responsible for interpreting and acting on their own state.
    """

    ROOT = Path.home() / ".config" / "wanderer"
    STATE_FILE = ROOT / "state.json"

    def __init__(self):

        self._state: dict[str, Any] = {}

        self.load()

    # =====================================================
    # Persistence
    # =====================================================

    def load(self) -> None:
        """Load persisted Wanderer state from disk."""

        if not self.STATE_FILE.exists():
            self._state = {}
            return

        try:
            with self.STATE_FILE.open(
                "r",
                encoding="utf-8"
            ) as file:
                data = json.load(file)

        except (
            OSError,
            json.JSONDecodeError
        ):
            self._state = {}
            return

        if isinstance(data, dict):
            self._state = data
        else:
            self._state = {}

    def save(self) -> bool:
        """Persist the current Wanderer state to disk."""

        try:
            self.ROOT.mkdir(
                parents=True,
                exist_ok=True
            )

            with self.STATE_FILE.open(
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(
                    self._state,
                    file,
                    indent=4
                )

        except OSError:
            return False

        return True

    # =====================================================
    # State Access
    # =====================================================

    def get(
        self,
        section: str,
        key: str,
        default=None
    ):
        """Return a value from a state section."""

        section_state = self._state.get(
            section,
            {}
        )

        if not isinstance(section_state, dict):
            return default

        return section_state.get(
            key,
            default
        )

    def set(
        self,
        section: str,
        key: str,
        value
    ) -> None:
        """Set a value in a state section."""

        section_state = self._state.setdefault(
            section,
            {}
        )

        if not isinstance(section_state, dict):
            section_state = {}
            self._state[section] = section_state

        section_state[key] = value

    # =====================================================
    # Section Access
    # =====================================================

    def get_section(
        self,
        section: str
    ) -> dict:
        """Return a copy of an entire state section."""

        section_state = self._state.get(
            section,
            {}
        )

        if not isinstance(section_state, dict):
            return {}

        return dict(section_state)

    def set_section(
        self,
        section: str,
        values: dict
    ) -> None:
        """Replace an entire state section."""

        self._state[section] = dict(values)

    # =====================================================
    # Maintenance
    # =====================================================

    def clear_section(
        self,
        section: str
    ) -> None:
        """Remove an entire state section."""

        self._state.pop(
            section,
            None
        )

    def clear(self) -> None:
        """Clear all in-memory state."""

        self._state.clear()