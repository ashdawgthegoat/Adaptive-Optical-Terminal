import platform

from PyQt6.QtCore import QObject

from Utils.system_info import SystemInfo


# ==========================================================
# Settings Application
#
# The first native application for WandererUI.
#
# Settings is a controller that drives the existing desktop
# panels directly. It does not create its own widgets or
# replace the desktop layout.
#
# Panels used:
#
#   NavigationPanel  — Displays settings categories and
#                      option lists.
#
#   Viewport         — Displays information about the
#                      currently selected setting.
#
#   ContextPanel     — Displays contextual metadata about
#                      the active category or selection.
#
#   Footer           — Displays keyboard shortcuts and
#                      current status.
#
# Services used:
#
#   Maaya   — Queries available themes, fonts and wallpapers.
#             Applies presentation changes.
#
#   Kaizen  — Locks and unlocks panel focus during sub-menu
#             navigation.
#
#   Animus  — Registers the application and manages its
#             lifecycle.
#
# ==========================================================


# ==========================================================
# Settings Categories
#
# Each category defines:
#
#   label   — The text shown in the NavigationPanel.
#
#   page    — An internal identifier used to determine
#             which page handler to invoke.
#
# ==========================================================

CATEGORIES = [

    {"label": "Appearance",  "page": "appearance"},
    {"label": "Wi-Fi",       "page": "wifi"},
    {"label": "Bluetooth",   "page": "bluetooth"},
    {"label": "Audio",       "page": "audio"},
    {"label": "Modules",     "page": "modules"},
    {"label": "About",       "page": "about"},

]


# ==========================================================
# Appearance Sub-Categories
# ==========================================================

APPEARANCE_ITEMS = [

    {"label": "Themes",     "page": "themes"},
    {"label": "Wallpapers", "page": "wallpapers"},
    {"label": "Fonts",      "page": "fonts"},

]


class SettingsApp(QObject):

    # ======================================================
    # Application Identity
    # ======================================================

    APP_ID = "settings"

    APP_NAME = "Settings"

    # ======================================================
    # Initialisation
    # ======================================================

    def __init__(
        self,
        maaya,
        kaizen,
        animus,
        navigation,
        viewport,
        context,
        footer
    ):

        super().__init__()

        # Core Services

        self.maaya = maaya
        self.kaizen = kaizen
        self.animus = animus

        # Desktop Panels

        self.navigation = navigation
        self.viewport = viewport
        self.context = context
        self.footer = footer

        # --------------------------------------------------
        # Navigation State
        #
        # Settings uses a simple depth model:
        #
        #   "categories"  — Root settings menu.
        #   "appearance"  — Appearance sub-categories.
        #   "themes"      — Theme option list.
        #   "wallpapers"  — Wallpaper option list.
        #   "fonts"       — Font option list.
        #
        # The depth determines how ESC behaves and what
        # ENTER activates.
        # --------------------------------------------------

        self.depth = "categories"

        # --------------------------------------------------
        # Registration
        #
        # The application registers itself with Animus so
        # the desktop environment is aware of its existence.
        # --------------------------------------------------

        self.animus.register_application({
            "id": self.APP_ID
        })

    # ======================================================
    # Lifecycle
    # ======================================================

    def launch(self):
        """
        Called when the desktop environment activates the
        Settings application.

        Sets up the initial navigation state and populates
        all panels with the root settings menu.
        """

        self.animus.launch(self.APP_ID)

        self.depth = "categories"

        self._show_categories()

    # ======================================================

    def close(self):
        """
        Called when the user exits the Settings application.

        Restores panel focus and cleans up application state.
        """

        self.kaizen.unlock()

        self.animus.close(self.APP_ID)

    # ======================================================
    # Input Handling
    #
    # The desktop shell forwards navigation events to the
    # active application. Settings interprets these events
    # based on its current depth.
    # ======================================================

    def handle_enter(self):
        """
        Activates the currently selected navigation item.

        Behaviour depends on the current depth.
        """

        selected = self.navigation.current_item()

        if selected is None:
            return

        if self.depth == "categories":

            self._activate_category(selected)

        elif self.depth == "appearance":

            self._activate_appearance_item(selected)

        elif self.depth == "themes":

            self._apply_theme(selected)

        elif self.depth == "wallpapers":

            self._apply_wallpaper(selected)

        elif self.depth == "fonts":

            self._apply_font(selected)

    # ======================================================

    def handle_escape(self):
        """
        Returns to the previous navigation depth.

        If already at the root, signals the desktop to
        close the application.
        """

        if self.depth == "categories":

            self.close()

            return

        if self.depth == "appearance":

            # Return to the root settings menu.

            self.depth = "categories"

            self._show_categories()

            return

        if self.depth in ("themes", "wallpapers", "fonts"):

            # Return to the appearance sub-menu.

            self.depth = "appearance"

            self._show_appearance()

            return

    # ======================================================
    # Root Menu
    # ======================================================

    def _show_categories(self):
        """
        Populates the panels with the root settings menu.
        """

        labels = [
            category["label"]
            for category in CATEGORIES
        ]

        self.navigation.set_items(labels)

        self.viewport.clear()

        self.viewport.show_ascii(
            "SETTINGS"
        )

        self.context.set_title("SETTINGS")

        self.context.set_info({
            "Application": self.APP_NAME,
            "Version": "1.0",
        })

        self.context.set_module_info({
            "Status": "Active"
        })

        self.footer.set_controls(
            "↑↓ Navigate    ENTER Select    ESC Close"
        )

        self.footer.set_status("Settings")

    # ======================================================

    def _activate_category(self, selected):
        """
        Handles selection of a root settings category.
        """

        # Find the page identifier for the selected label.

        page = self._page_for_label(
            CATEGORIES,
            selected
        )

        if page == "appearance":

            self.depth = "appearance"

            self._show_appearance()

        elif page == "wifi":

            self._show_placeholder("Wi-Fi")

        elif page == "bluetooth":

            self._show_placeholder("Bluetooth")

        elif page == "audio":

            self._show_placeholder("Audio")

        elif page == "modules":

            self._show_placeholder("Modules")

        elif page == "about":

            self._show_about()

    # ======================================================
    # Appearance Menu
    # ======================================================

    def _show_appearance(self):
        """
        Populates the panels with the appearance sub-menu.
        """

        labels = [
            item["label"]
            for item in APPEARANCE_ITEMS
        ]

        self.navigation.set_items(labels)

        self.viewport.clear()

        self.viewport.show_ascii(
            "APPEARANCE"
        )

        self.context.set_title("APPEARANCE")

        self.context.set_info({
            "Theme": self._current_theme_name(),
            "Font": self._current_font_name(),
        })

        self.context.set_module_info({
            "Status": "Active"
        })

        self.footer.set_controls(
            "↑↓ Navigate    ENTER Select    ESC Back"
        )

        self.footer.set_status("Appearance")

    # ======================================================

    def _activate_appearance_item(self, selected):
        """
        Handles selection of an appearance sub-category.
        """

        page = self._page_for_label(
            APPEARANCE_ITEMS,
            selected
        )

        if page == "themes":

            self.depth = "themes"

            self._show_themes()

        elif page == "wallpapers":

            self.depth = "wallpapers"

            self._show_wallpapers()

        elif page == "fonts":

            self.depth = "fonts"

            self._show_fonts()

    # ======================================================
    # Themes
    # ======================================================

    def _show_themes(self):
        """
        Lists all available themes from Maaya.
        """

        themes = self.maaya.available_themes()

        if not themes:

            self._show_empty_list("Themes")

            return

        self.navigation.set_items(themes)

        self.viewport.clear()

        self.viewport.show_ascii(
            "SELECT THEME"
        )

        self.context.set_title("THEMES")

        self.context.set_info({
            "Active Theme": self._current_theme_name(),
            "Available": str(len(themes)),
        })

        self.context.set_module_info({
            "Status": "Active"
        })

        self.footer.set_controls(
            "↑↓ Navigate    ENTER Apply    ESC Back"
        )

        self.footer.set_status("Themes")

    # ======================================================

    def _apply_theme(self, package):
        """
        Loads the selected theme through Maaya.
        """

        result = self.maaya.load_theme(package)

        if result is None:

            self.footer.set_status(
                f"Failed to load theme: {package}"
            )

            return

        self.footer.set_status(
            f"Applied: {package}"
        )

        # Refresh the context panel to reflect the change.

        self.context.set_info({
            "Active Theme": self._current_theme_name(),
            "Available": str(
                len(self.maaya.available_themes())
            ),
        })

    # ======================================================
    # Wallpapers
    # ======================================================

    def _show_wallpapers(self):
        """
        Lists all available static wallpapers from Maaya.
        """

        wallpapers = self.maaya.available_wallpapers(
            "static"
        )

        if not wallpapers:

            self._show_empty_list("Wallpapers")

            return

        self.navigation.set_items(wallpapers)

        self.viewport.clear()

        self.viewport.show_ascii(
            "SELECT WALLPAPER"
        )

        self.context.set_title("WALLPAPERS")

        self.context.set_info({
            "Active": self._current_wallpaper_name(),
            "Available": str(len(wallpapers)),
        })

        self.context.set_module_info({
            "Status": "Active"
        })

        self.footer.set_controls(
            "↑↓ Navigate    ENTER Apply    ESC Back"
        )

        self.footer.set_status("Wallpapers")

    # ======================================================

    def _apply_wallpaper(self, filename):
        """
        Loads the selected wallpaper through Maaya and
        displays it in the Viewport.
        """

        result = self.maaya.load_wallpaper(
            "static",
            filename
        )

        if result is None:

            self.footer.set_status(
                f"Failed to load wallpaper: {filename}"
            )

            return

        # Display the wallpaper in the Viewport.

        self.viewport.show_wallpaper()

        self.footer.set_status(
            f"Applied: {filename}"
        )

        self.context.set_info({
            "Active": self._current_wallpaper_name(),
            "Available": str(
                len(
                    self.maaya.available_wallpapers("static")
                )
            ),
        })

    # ======================================================
    # Fonts
    # ======================================================

    def _show_fonts(self):
        """
        Lists all available font packages from Maaya.
        """

        fonts = self.maaya.available_fonts()

        if not fonts:

            self._show_empty_list("Fonts")

            return

        self.navigation.set_items(fonts)

        self.viewport.clear()

        self.viewport.show_ascii(
            "SELECT FONT"
        )

        self.context.set_title("FONTS")

        self.context.set_info({
            "Active Font": self._current_font_name(),
            "Available": str(len(fonts)),
        })

        self.context.set_module_info({
            "Status": "Active"
        })

        self.footer.set_controls(
            "↑↓ Navigate    ENTER Apply    ESC Back"
        )

        self.footer.set_status("Fonts")

    # ======================================================

    def _apply_font(self, package):
        """
        Loads the selected font package through Maaya.
        """

        result = self.maaya.load_font(package)

        if result is None:

            self.footer.set_status(
                f"Failed to load font: {package}"
            )

            return

        self.footer.set_status(
            f"Applied: {package}"
        )

        self.context.set_info({
            "Active Font": self._current_font_name(),
            "Available": str(
                len(self.maaya.available_fonts())
            ),
        })

    # ======================================================
    # About Page
    # ======================================================

    def _show_about(self):
        """
        Displays system information on the About page.

        Uses the SystemInfo utility directly rather than
        going through a service.
        """

        self.viewport.clear()

        self.viewport.show_ascii(
            "ABOUT WANDERER"
        )

        self.context.set_title("ABOUT")

        self.context.set_info({
            "Hostname": SystemInfo.hostname(),
            "Platform": platform.system(),
            "CPU": SystemInfo.cpu(),
            "Memory": SystemInfo.memory(),
            "Storage": SystemInfo.storage(),
            "Battery": SystemInfo.battery(),
        })

        self.context.set_module_info({
            "Status": SystemInfo.status()
        })

        self.footer.set_controls(
            "↑↓ Navigate    ESC Back"
        )

        self.footer.set_status("About")

    # ======================================================
    # Placeholder Pages
    # ======================================================

    def _show_placeholder(self, name):
        """
        Displays a placeholder page for sections that are
        not yet implemented.
        """

        self.viewport.clear()

        self.viewport.show_ascii(
            f"{name.upper()}\n\n"
            f"This section is not yet available."
        )

        self.context.set_title(name.upper())

        self.context.set_info({
            "Status": "Not Available"
        })

        self.context.set_module_info({
            "Status": "Placeholder"
        })

        self.footer.set_controls(
            "↑↓ Navigate    ESC Back"
        )

        self.footer.set_status(name)

    # ======================================================
    # Empty List Fallback
    # ======================================================

    def _show_empty_list(self, name):
        """
        Handles the case where a category has no available
        options to display.
        """

        self.navigation.set_items([])

        self.viewport.clear()

        self.viewport.show_ascii(
            f"No {name.lower()} available."
        )

        self.footer.set_status(
            f"No {name.lower()} found"
        )

    # ======================================================
    # Utilities
    # ======================================================

    def _page_for_label(self, items, label):
        """
        Returns the page identifier for a given navigation
        label within a list of category dictionaries.
        """

        for item in items:

            if item["label"] == label:

                return item["page"]

        return None

    # ======================================================

    def _current_theme_name(self):
        """
        Returns the name of the currently active theme.
        """

        if self.maaya.theme is None:

            return "None"

        if hasattr(self.maaya.theme, "Theme"):

            return self.maaya.theme.Theme.NAME

        return "Unknown"

    # ======================================================

    def _current_font_name(self):
        """
        Returns the family name of the currently active font.
        """

        if self.maaya.font is None:

            return "None"

        return self.maaya.font.get(
            "family",
            "Unknown"
        )

    # ======================================================

    def _current_wallpaper_name(self):
        """
        Returns the filename of the currently active
        wallpaper.
        """

        if self.maaya.wallpaper is None:

            return "None"

        return self.maaya.wallpaper.get(
            "filename",
            "Unknown"
        )
