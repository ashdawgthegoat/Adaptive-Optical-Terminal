from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout
)

from PyQt6.QtCore import Qt
from widgets.theme import (
    PRIMARY,
    BODY_FONT,
    SECTION_FONT,
    ACCENT
)

from services.maaya import Maaya
from widgets.panel import Panel

class Viewport(Panel):

    def __init__(self):
        super().__init__()

        self.title = QLabel("VIEWPORT")

        self.display = QLabel()

        self.maaya = Maaya()

        self.maaya.frame_changed.connect(
            self.show_ascii
        )

        self.build_ui()

    def build_ui(self):

        layout = QVBoxLayout()

        layout.setContentsMargins(10, 10, 10, 10)

        layout.setSpacing(0)

        self.title.setFont(SECTION_FONT)
        self.title.setStyleSheet(f"color: {PRIMARY};")
        self.title.setAlignment(Qt.AlignmentFlag.AlignLeft)

        layout.addWidget(self.title)

        layout.addStretch()

        self.display.setFont(BODY_FONT)

        self.display.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.display.setStyleSheet(
            f"color: {PRIMARY};"
        )

        self.show_ascii(self.maaya.get_logo("wanderer"))

        layout.addWidget(
            self.display,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        layout.addStretch()

        self.setLayout(layout)

        self.set_inactive()

    def show_ascii(self,ascii_art):

        self.display.setText(
            ascii_art
        )
    
    def play_animation(self, name, fps=10):

        self.maaya.set_fps(fps)

        self.maaya.set_animation(name)

        self.maaya.play()

    def clear(self):

        self.display.clear()