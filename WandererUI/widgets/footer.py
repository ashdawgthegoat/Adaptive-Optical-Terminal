from PyQt6.QtWidgets import (
    QLabel,
    QHBoxLayout
)

from PyQt6.QtGui import QFont

from widgets.layer.panel import Panel

# ==========================================================
# Footer
#
# Displays global controls and the current system status.
#
# This panel participates in the focus system and renders
# the standard panel border.
# ==========================================================

class Footer(Panel):

    def __init__(
        self,
        maaya,
        controls="↑↓ Navigate    ENTER Select    ESC Back",
        status="Ready."
    ):

        super().__init__(
            maaya,
            show_border=True
        )

        self.maaya = maaya

        self.palette = self.maaya.theme.Palette

        self.typography = self.maaya.typography()

        self.controls = QLabel(controls)

        self.status = QLabel(status)

        self.build_ui()

    # ==========================================================
    # UI Construction
    # ==========================================================

    def build_ui(self):

        footer_font = QFont(
            self.maaya.font["family"],
            self.typography.FOOTER_SIZE
        )

        self.controls.setFont(footer_font)

        self.status.setFont(footer_font)

        self.controls.setStyleSheet(
            f"color: {self.palette.SECONDARY};"
        )

        self.status.setStyleSheet(
            f"color: {self.palette.PRIMARY};"
        )

        layout = QHBoxLayout()

        padding = self.content_padding()

        layout.setContentsMargins(
            padding,    
            padding,
            padding,
            padding
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

    # ==========================================================
    # Footer Content
    # ==========================================================

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