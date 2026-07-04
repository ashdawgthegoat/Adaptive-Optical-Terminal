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

        self.setCentralWidget(
            self.desktop
        )

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setFocus()

        # ==================================================
        # Discover Applications
        # ==================================================

        self.animus.discover_applications()

    def keyPressEvent(self, event):

        key = event.key()

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


def main():

    app = QApplication(sys.argv)

    window = MainWindow()

    window.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":

    main()