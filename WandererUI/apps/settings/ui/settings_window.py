# =============================================================================
# Settings Application — Main Window
# =============================================================================
#
# Top-level QMainWindow housing the Sidebar, QStackedWidget of pages,
# and StatusBar. Manages focus switching between sidebar and active page.
#
# =============================================================================

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QStackedWidget, QFrame,
)
from PyQt6.QtCore import Qt

from .theme import Palette, FONT_FAMILY
from .sidebar import Sidebar
from .status_bar import StatusBar
from .pages.base_page import BasePage
from .pages.appearance_page import AppearancePage
from .pages.wifi_page import WifiPage
from .pages.bluetooth_page import BluetoothPage
from .pages.audio_page import AudioPage
from .pages.modules_page import ModulesPage
from .pages.about_page import AboutPage


# =============================================================================
# Category Definitions
# =============================================================================

CATEGORIES = [
    "Appearance",
    "Wi-Fi",
    "Bluetooth",
    "Audio",
    "Modules",
    "About",
]


# =============================================================================
# SettingsWindow
# =============================================================================

class SettingsWindow(QMainWindow):
    """Main settings window.

    Layout: Sidebar (left) | Pages (right, stacked) | StatusBar (bottom).
    Tab toggles focus between sidebar and the active page.
    Escape moves focus to sidebar or closes the window.
    """

    MIN_WIDTH = 900
    MIN_HEIGHT = 600
    DEFAULT_WIDTH = 1100
    DEFAULT_HEIGHT = 700

    # =========================================================================
    # Construction
    # =========================================================================

    def __init__(self, controller, maaya, providers: dict, parent=None) -> None:
        super().__init__(parent)

        self._controller = controller
        self._maaya = maaya
        self._providers = providers
        self._focus_on_sidebar = True

        self._configure_window()
        self._build_ui()
        self._connect_signals()

        # Start on first page
        self._switch_page(0)
        self._sidebar.setFocus()

    # =========================================================================
    # Keyboard Handling
    # =========================================================================

    def keyPressEvent(self, event) -> None:
        """Handle top-level keyboard shortcuts."""
        key = event.key()

        if key == Qt.Key.Key_Tab:
            self._toggle_focus()

        elif key == Qt.Key.Key_Escape:
            if not self._focus_on_sidebar:
                # Move focus to sidebar
                self._focus_on_sidebar = True
                self._sidebar.setFocus()
                self._update_status_hints()
            else:
                # Close window
                self.close()

        elif key == Qt.Key.Key_Backtab:
            # Shift+Tab also toggles focus
            self._toggle_focus()

        else:
            super().keyPressEvent(event)

    # =========================================================================
    # Internal — Window Configuration
    # =========================================================================

    def _configure_window(self) -> None:
        """Set window title, size, and background."""
        self.setWindowTitle("Settings")
        self.setMinimumSize(self.MIN_WIDTH, self.MIN_HEIGHT)
        self.resize(self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT)
        self.setStyleSheet(f"background-color: {Palette.BACKGROUND};")

    # =========================================================================
    # Internal — UI Construction
    # =========================================================================

    def _build_ui(self) -> None:
        """Build the window layout: sidebar + pages + status bar."""
        central = QWidget(self)
        self.setCentralWidget(central)

        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # --- Top area: sidebar + pages ---
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(0)

        # Sidebar
        self._sidebar = Sidebar(CATEGORIES, central)

        # Vertical separator line
        separator = QFrame(central)
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setFixedWidth(1)
        separator.setStyleSheet(f"background-color: {Palette.SEPARATOR};")

        # Stacked pages
        self._stack = QStackedWidget(central)
        self._pages: list[BasePage] = []
        self._create_pages()

        top_layout.addWidget(self._sidebar)
        top_layout.addWidget(separator)
        top_layout.addWidget(self._stack, 1)

        root_layout.addLayout(top_layout, 1)

        # --- Status bar ---
        self._status_bar = StatusBar(central)
        root_layout.addWidget(self._status_bar)

    def _create_pages(self) -> None:
        """Instantiate all pages and add them to the stacked widget."""
        # 0 — Appearance
        appearance = AppearancePage(

            self._controller,
            self._maaya,
            )
        self._add_page(appearance)

        # 1 — Wi-Fi
        self._add_page(WifiPage())

        # 2 — Bluetooth
        self._add_page(BluetoothPage())

        # 3 — Audio
        self._add_page(AudioPage())

        # 4 — Modules
        self._add_page(ModulesPage())

        # 5 — About
        about = AboutPage(self._providers["system_info"])
        self._add_page(about)

    def _add_page(self, page: BasePage) -> None:
        """Register a page in the stack and internal list."""
        self._pages.append(page)
        self._stack.addWidget(page)

    # =========================================================================
    # Internal — Signal Connections
    # =========================================================================

    def _connect_signals(self) -> None:
        """Wire up sidebar, controller, and page signals."""
        self._sidebar.category_changed.connect(self._on_category_changed)
        self._controller.page_changed.connect(self._on_controller_page_changed)
        self._controller.theme_changed.connect(self._on_theme_changed)
        self._controller.font_changed.connect(self._on_font_changed)

    # =========================================================================
    # Internal — Page Switching
    # =========================================================================

    def _on_category_changed(self, index: int) -> None:
        """Handle sidebar selection change."""
        self._controller.set_current_page(index)

    def _on_controller_page_changed(self, index: int) -> None:
        """Handle controller page change signal."""
        self._switch_page(index)

    def _switch_page(self, index: int) -> None:
        """Switch the active page in the stacked widget."""
        if not (0 <= index < len(self._pages)):
            return

        # Leave old page
        old_index = self._stack.currentIndex()
        if 0 <= old_index < len(self._pages):
            self._pages[old_index].on_leave()

        # Switch
        self._stack.setCurrentIndex(index)
        self._sidebar.set_selected_index(index)

        # Enter new page
        self._pages[index].on_enter()

        # Update status bar
        self._update_status_hints()

    # =========================================================================
    # Internal — Focus Management
    # =========================================================================

    def _toggle_focus(self) -> None:
        """Toggle focus between sidebar and the active page."""
        if self._focus_on_sidebar:
            self._focus_on_sidebar = False
            current_page = self._pages[self._stack.currentIndex()]
            current_page.setFocus()
        else:
            self._focus_on_sidebar = True
            self._sidebar.setFocus()

        self._update_status_hints()

    def _update_status_hints(self) -> None:
        """Update the status bar hints based on current focus."""
        if self._focus_on_sidebar:
            self._status_bar.set_hints(
                "↑↓ Navigate   Tab Page   Q Quit"
            )
        else:
            page = self._pages[self._stack.currentIndex()]
            self._status_bar.set_hints(page.hint_text())

    # =========================================================================
    # Internal — Live Updates
    # =========================================================================

    def _on_theme_changed(self, name: str) -> None:
        """Handle theme change from the controller."""
        self._status_bar.set_status(f"Theme: {name}")

    def _on_font_changed(self, family: str) -> None:
        """Handle font change from the controller."""
        self._status_bar.set_status(f"Font: {family}")
