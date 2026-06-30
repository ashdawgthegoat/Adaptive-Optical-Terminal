from PyQt6.QtWidgets import (
    QLabel,
    QHBoxLayout
)

from PyQt6.QtGui import QFont

from widgets.panel import Panel


class Footer(Panel):

    def __init__(
        self,
        maaya,
        controls="↑↓ Navigate    ENTER Select    ESC Back",
        status="Ready."
    ):

        super().__init__(maaya)

        self.maaya = maaya

        self.palette = self.maaya.theme.Palette

        self.typography = self.maaya.typography()

        self.controls = QLabel(controls)

        self.status = QLabel(status)

        self.build_ui()

    def build_ui(self):

        font = QFont(
            self.maaya.font["family"],
            self.typography.FOOTER_SIZE
        )

        self.controls.setFont(font)

        self.status.setFont(font)

        self.controls.setStyleSheet(
            f"color: {self.palette.SECONDARY};"
        )

        self.status.setStyleSheet(
            f"color: {self.palette.PRIMARY};"
        )

        layout = QHBoxLayout()

        layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        layout.addWidget(
            self.controls
        )

        layout.addStretch()

        layout.addWidget(
            self.status
        )

        self.setLayout(
            layout
        )

        self.set_inactive()

    def set_controls(
        self,
        text
    ):

        self.controls.setText(
            text
        )

    def set_status(
        self,
        text
    ):

        self.status.setText(
            text
        )