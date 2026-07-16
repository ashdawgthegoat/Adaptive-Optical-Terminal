import sys

from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow
)

from services.maaya import Maaya
from services.kaizen import Kaizen
from services.animus import Animus

from widgets.desktop import Desktop


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        # ==================================================
        # Window
        # ==================================================

        self.setWindowTitle("WandererUI")

        self.showFullScreen()

        self.setStyleSheet(
            "background-color: black;"
        )

        # ==================================================
        # Core Services
        # ==================================================

        self.maaya = Maaya()

        # --------------------------------------------------
        # Temporary default presentation package
        # Will later be restored by Eidolon / Settings
        # --------------------------------------------------

        self.maaya.load_theme("classic")
        self.maaya.load_font("system")
        wallpapers = self.maaya.available_wallpapers(
            "static"
        )

        if wallpapers:

            self.maaya.load_wallpaper(
                "static",
                wallpapers[0]
            )

        self.animus = Animus(
            development_mode=True
        )

        self.kaizen = Kaizen()

        # ==================================================
        # Desktop
        # ==================================================

        self.desktop = Desktop(
            self.maaya,
            self.animus,
            self.kaizen
        )

        self.animus.desktop_launch_requested.connect(
            self.launch_core_application
        )

        self.animus.workbench_launch_requested.connect(
            self.launch_workbench_application
        )

        self.setCentralWidget(
            self.desktop
        )

        self.kaizen.initialize()

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setFocus()

        # ==================================================
        # Discover Applications
        # ==================================================

        self.animus.discover_applications()

    def keyPressEvent(self, event):

        key = event.key()

        if self.desktop.overlay_visible():

            if key == Qt.Key.Key_Up:

                self.desktop.overlay.move_up()

                return

            elif key == Qt.Key.Key_Down:

                self.desktop.overlay.move_down()

                return

            elif key in (
                Qt.Key.Key_Return,
                Qt.Key.Key_Enter
            ):

                self.desktop.overlay.activate()

                return

            elif key == Qt.Key.Key_Escape:

                self.desktop.hide_overlay()

                return

        if key == Qt.Key.Key_Control:

            locked = self.kaizen.toggle_lock()

            if locked:

                self.desktop.footer.set_status(
                    f"{self.kaizen.current().upper()} Captured"
                )

            else:

                self.desktop.footer.set_status(
                    "Panel Navigation"
                )

            return

        if self.kaizen.is_locked():

            panel = self.desktop.current_panel()

            if key == Qt.Key.Key_Left:

                panel.move_left()

            elif key == Qt.Key.Key_Right:

                panel.move_right()

            elif key == Qt.Key.Key_Up:

                panel.move_up()

            elif key == Qt.Key.Key_Down:

                panel.move_down()

            elif key in (
                Qt.Key.Key_Return,
                Qt.Key.Key_Enter
            ):

                if self.kaizen.has_focus("context"):

                    self.desktop.activate_context_item()

                else:

                    panel.activate()

        else:

            if key == Qt.Key.Key_Left:

                self.kaizen.move_left()

            elif key == Qt.Key.Key_Right:

                self.kaizen.move_right()

            elif key == Qt.Key.Key_Up:

                self.kaizen.move_up()

            elif key == Qt.Key.Key_Down:

                self.kaizen.move_down()

            else:

                super().keyPressEvent(event)

    def launch_core_application(self, application):
        """Launch a Core Application."""

        print("[3] desktop_launch_requested")

        desktop_application = (
            self.animus.create_desktop_application(
                application,
                self.maaya
            )
        )

        if desktop_application is None:
            return

        self.desktop.enter_application(
            desktop_application
        )


    def launch_workbench_application(self, application):
        """Launch a Workbench application."""

        print(
            f"[Workbench] Launching {application['name']}"
        )


def main():

    app = QApplication(sys.argv)

    window = MainWindow()

    window.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":

    main()