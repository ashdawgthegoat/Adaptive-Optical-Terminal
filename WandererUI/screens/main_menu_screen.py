from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout
)

from PyQt6.QtCore import Qt

from widgets.main_layout import MainLayout

from services.viewport_manager import ViewportManager
from services.context_manager import ContextManager
from services.kaizen import Kaizen


class MainMenuScreen(QWidget):

    def __init__(self):

        super().__init__()

        self.enter_callback = None

        self.setFocusPolicy(
            Qt.FocusPolicy.StrongFocus
        )

        self.ui = MainLayout()

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

        self.viewport_manager.show_animation(
            "stars",
            fps=5
        )

        self.ui.navigation.set_items([
            "OBSERVE",
            "ARCHIVE",
            "MUSIC",
            "MODULES",
            "SETTINGS"
        ])

        self.context_manager.start()

        self.ui.footer.set_controls(
            "↑↓ Navigate    ENTER Select"
        )

        self.ui.footer.set_status(
            "Ready."
        )

        self.kaizen.register("header")
        self.kaizen.register("navigation")
        self.kaizen.register("viewport")
        self.kaizen.register("context")
        self.kaizen.register("footer")

        self.kaizen.initialize()
        self.update_focus()

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

        if event.key() == Qt.Key.Key_Tab:

            self.kaizen.next()
            self.update_focus()

            print(
                self.kaizen.current()
            )

            return

        if (
            self.kaizen.has_focus("navigation")
            and event.key() == Qt.Key.Key_Up
        ):

            self.ui.navigation.move_up()

        elif (
            self.kaizen.has_focus("navigation")
            and event.key() == Qt.Key.Key_Down
        ):

            self.ui.navigation.move_down()

        elif (
            self.kaizen.has_focus("navigation")
            and event.key() in (
                Qt.Key.Key_Return,
                Qt.Key.Key_Enter
            )
        ):

            if self.enter_callback:

                self.enter_callback(
                    self.ui.navigation.current_item()
                )

        else:

            super().keyPressEvent(event)