from PyQt6.QtWidgets import (
    QLabel,
    QHBoxLayout,
)

from PyQt6.QtCore import (
    Qt,
    pyqtSignal,
)

from PyQt6.QtGui import QFont

from widgets.layer.panel import Panel


class EnvironmentWidget(Panel):

    # Emitted when the user activates this widget.
    # Later this will cycle through themes, wallpapers
    # and typography presets.
    activated = pyqtSignal()

    def __init__(self, maaya):

        super().__init__(maaya, show_border=False)

        self.maaya = maaya

        self.palette = self.maaya.theme.Palette

        self.spacing = self.maaya.theme.Spacing

        self.typography = self.maaya.typography()

        self.build_ui()

    def build_ui(self):

        # Placeholder environment controls.
        # These will later become interactive controls
        # for Maaya.
        self.environment = QLabel(
            "🎨  🖼  Aa"
        )

        self.environment.setFont(
            QFont(
                self.maaya.font["family"],
                self.typography.BODY_SIZE
            )
        )

        self.environment.setStyleSheet(
            f"color: {self.palette.PRIMARY};"
        )

        self.environment.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout = QHBoxLayout()

        layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        layout.setSpacing(
            self.spacing.ITEM_SPACING
        )

        layout.addWidget(
            self.environment
        )

        self.setLayout(
            layout
        )

        self.set_inactive()

    def refresh_presentation(self):

        self.palette = self.maaya.theme.Palette

        self.spacing = self.maaya.theme.Spacing

        self.typography = self.maaya.typography()

        self.environment.setFont(
            QFont(
                self.maaya.font["family"],
                self.typography.BODY_SIZE
            )
        )

        self.environment.setStyleSheet(
            f"color: {self.palette.PRIMARY};"
        )

        self.update()

    def keyPressEvent(
        self,
        event
    ):

        if event.key() in (
            Qt.Key.Key_Return,
            Qt.Key.Key_Enter,
        ):

            self.activated.emit()

        else:

            super().keyPressEvent(
                event
            )

    def mousePressEvent(
        self,
        event
    ):

        if event.button() == Qt.MouseButton.LeftButton:

            self.activated.emit()

        super().mousePressEvent(
            event
        )