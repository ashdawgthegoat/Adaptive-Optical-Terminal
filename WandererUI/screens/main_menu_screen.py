from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout
)

from PyQt6.QtCore import Qt

from widgets.main_layout import MainLayout

from services.viewport_manager import ViewportManager
from services.context_manager import ContextManager
from services.kaizen import Kaizen
from services.maaya import Maaya

class MainMenuScreen(QWidget):

    def __init__(self):

        super().__init__()

        self.enter_callback = None

        self.setFocusPolicy(
            Qt.FocusPolicy.StrongFocus
        )

        self.maaya = Maaya()

        self.maaya.load_theme(
            "classic"
        )

        self.maaya.load_font(
            "system"
        )

        self.maaya.load_wallpaper(
            "static",
            "Reze.txt"
        )

        self.ui = MainLayout(self.maaya)

        self.viewport_manager = ViewportManager(
            self.ui.viewport
        )

        self.context_manager = ContextManager(
            self.ui.context
        )

        self.kaizen = Kaizen()

        layout = QVBoxLayout()

        layout.addWidget(
            self.ui
        )

        self.setLayout(
            layout
        )

        self.initialize_screen()

    def initialize_screen(self):

        self.ui.header.set_title(
            "WANDERER",
            "MK II Alpha"
        )

        self.ui.viewport.show_wallpaper()

        self.ui.navigation.set_items([
            "OBSERVE",
            "ARCHIVE",
            "MUSIC",
            "MODULES",
            "SETTINGS"
        ])

        self.context_manager.start()

        self.ui.footer.set_controls(
            "←↑↓→ Navigate    CTRL Capture    ENTER Select"
        )

        self.ui.footer.set_status(
            "Ready."
        )

        self.kaizen.focus_changed.connect(
            lambda _: self.update_focus()
        )

        self.ui.header.clicked.connect(
            lambda: self.change_focus("header")
        )

        self.ui.navigation.clicked.connect(
            lambda: self.change_focus("navigation")
        )

        self.ui.viewport.clicked.connect(
            lambda: self.change_focus("viewport")
        )

        self.ui.context.clicked.connect(
            lambda: self.change_focus("context")
        )

        self.ui.footer.clicked.connect(
            lambda: self.change_focus("footer")
        )

        self.kaizen.initialize()

    def change_focus(self, region):

        self.kaizen.set_focus(region)

        self.setFocus()

    def update_focus(self):

        self.ui.header.set_inactive()
        self.ui.navigation.set_inactive()
        self.ui.viewport.set_inactive()
        self.ui.context.set_inactive()
        self.ui.footer.set_inactive()

        match self.kaizen.current():

            case "header":
                self.ui.header.set_active()

            case "navigation":
                self.ui.navigation.set_active()

            case "viewport":
                self.ui.viewport.set_active()

            case "context":
                self.ui.context.set_active()

            case "footer":
                self.ui.footer.set_active()

    def keyPressEvent(self, event):

    # ==========================
    # Toggle panel capture
    # ==========================

        if event.key() == Qt.Key.Key_Control:

            locked = self.kaizen.toggle_lock()

            if locked:

                self.ui.footer.set_status(
                    f"{self.kaizen.current().upper()} Captured"
                )

            else:

                self.ui.footer.set_status(
                    "Panel Navigation"
                )

            return

    # ==========================
    # Panel Navigation
    # ==========================

        if not self.kaizen.is_locked():

            match event.key():

                case Qt.Key.Key_Left:

                    self.kaizen.move_left()
                    return

                case Qt.Key.Key_Right:

                    self.kaizen.move_right()
                    return

                case Qt.Key.Key_Up:

                    self.kaizen.move_up()
                    return

                case Qt.Key.Key_Down:

                    self.kaizen.move_down()
                    return

    # ==========================
    # Navigation Panel
    # ==========================

        if self.kaizen.has_focus("navigation"):

            if event.key() == Qt.Key.Key_Up:

                self.ui.navigation.move_up()
                return

            elif event.key() == Qt.Key.Key_Down:

                self.ui.navigation.move_down()
                return

            elif event.key() in (
                Qt.Key.Key_Return,
                Qt.Key.Key_Enter
            ):

                if self.enter_callback:

                    self.enter_callback(
                        self.ui.navigation.current_item()
                    )

                return

        super().keyPressEvent(event)