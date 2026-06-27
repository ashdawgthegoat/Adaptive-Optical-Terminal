from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout
)

from PyQt6.QtCore import Qt
from widgets.theme import (
    PRIMARY,
    BODY_FONT
)

from services.ascii_loader import (load_ascii)

class Viewport(QWidget):

    def __init__(self):
        super().__init__()

        self.display = QLabel()

        self.build_ui()

    def build_ui(self):

        layout = QVBoxLayout()

        layout.setContentsMargins(0, 0, 0, 0)

        layout.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.display.setFont(BODY_FONT)

        self.display.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.display.setStyleSheet(
            f"color: {PRIMARY};"
        )

        self.show_ascii(load_ascii("wanderer"))

        layout.addWidget(
            self.display
        )

        self.setLayout(
            layout
        )

    def show_ascii(self,ascii_art):

        self.display.setText(
            ascii_art
        )

    def clear(self):

        self.display.clear()