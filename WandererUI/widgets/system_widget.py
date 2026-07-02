from PyQt6.QtWidgets import (
    QLabel,
    QHBoxLayout,
)

from PyQt6.QtCore import (
    Qt,
    pyqtSignal,
)

from PyQt6.QtGui import QFont

from widgets.panel import Panel


class SystemWidget(Panel):

    # Emitted when the user activates this widget.
    # Later this can open the Power Menu or System Menu.
    activated = pyqtSignal()

    def __init__(self, maaya):

        super().__init__(maaya, show_border=False)

        self.maaya = maaya

        self.palette = self.maaya.theme.Palette

        self.spacing = self.maaya.theme.Spacing

        self.typography = self.maaya.typography()

        self.build_ui()

    def build_ui(self):

        # Placeholder system indicators.
        # These will later be replaced with live providers.
        self.system = QLabel(
            "📶  🔊  🔋  ⏻"
        )

        self.system.setFont(
            QFont(
                self.maaya.font["family"],
                self.typography.BODY_SIZE
            )
        )

        self.system.setStyleSheet(
            f"color: {self.palette.PRIMARY};"
        )

        self.system.setAlignment(
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
            self.system
        )

        self.setLayout(
            layout
        )

        self.set_inactive()

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