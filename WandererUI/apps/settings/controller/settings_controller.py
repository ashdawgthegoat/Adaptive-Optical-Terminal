from PyQt6.QtCore import QObject, pyqtSignal


# ==========================================================
# Settings Controller
#
# Manages application state for the Settings app.
#
# This controller tracks:
#
#   - The currently visible page index.
#   - The active theme, wallpaper and font selections.
#
# It emits signals when any of these values change so that
# the UI layer can react accordingly.
#
# This controller does NOT handle keyboard navigation or
# focus management. Those concerns belong to the shell.
# ==========================================================


class SettingsController(QObject):

    # ======================================================
    # Signals
    # ======================================================

    page_changed = pyqtSignal(str)

    theme_changed = pyqtSignal(str)

    wallpaper_changed = pyqtSignal(str)

    font_changed = pyqtSignal(str)

    # ======================================================
    # Initialisation
    # ======================================================

    def __init__(self, parent=None):

        super().__init__(parent)

        self._current_page = "Appearance"
        self._active_theme: str | None = None
        self._active_wallpaper: str | None = None
        self._active_font: str | None = None

    # ======================================================
    # Properties
    # ======================================================

    @property
    def current_page(self):

        return self._current_page

    # ======================================================

    @property
    def active_theme(self) -> str | None:
        """
        Returns the name of the currently active theme,
        or None if no theme is set.
        """

        return self._active_theme

    # ======================================================

    @property
    def active_wallpaper(self) -> str | None:
        """
        Returns the name of the currently active wallpaper,
        or None if no wallpaper is set.
        """

        return self._active_wallpaper

    # ======================================================

    @property
    def active_font(self) -> str | None:
        """
        Returns the family name of the currently active
        font, or None if no font is set.
        """

        return self._active_font

    # ======================================================
    # Setters
    # ======================================================

    def set_current_page(self, page: str):
        
        if page == self._current_page:

            return

        self._current_page = page

        self.page_changed.emit(page)

    # ======================================================

    def set_active_theme(self, name: str):
        """
        Sets the active theme name and emits theme_changed.
        """

        self._active_theme = name

        self.theme_changed.emit(name)

    # ======================================================

    def set_active_wallpaper(self, name: str):
        """
        Sets the active wallpaper name and emits
        wallpaper_changed.
        """

        self._active_wallpaper = name

        self.wallpaper_changed.emit(name)

    # ======================================================

    def set_active_font(self, family: str):
        """
        Sets the active font family and emits font_changed.
        """

        self._active_font = family

        self.font_changed.emit(family)
