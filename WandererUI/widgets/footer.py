from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout
)

from PyQt6.QtCore import Qt
from widgets.theme import (
    SMALL_FONT,
    PRIMARY,
    SECONDARY,
)


class Footer(QWidget):

    def __init__(
        self,
        controls="↑↓ Navigate    ENTER Select    ESC Back",
        status="Ready."
    ):
        super().__init__()

        self.controls = QLabel(controls)
        self.status = QLabel(status)

        self.build_ui()

    def build_ui(self):

        self.controls.setFont(SMALL_FONT)
        self.status.setFont(SMALL_FONT)

        self.controls.setStyleSheet(
            f"color: {SECONDARY};"
        )

        self.status.setStyleSheet(
            f"color: {PRIMARY};"
        )

        layout = QHBoxLayout()

        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(
            self.controls
        )

        layout.addStretch()

        layout.addWidget(
            self.status
        )

        self.setLayout(layout)

    def set_controls(
        self,
        text
    ):

        self.controls.setText(text)

    def set_status(
        self,
        text
    ):

        self.status.setText(text)