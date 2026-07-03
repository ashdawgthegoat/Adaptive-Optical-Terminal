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


class RuntimeWidget(Panel):

    # Emitted when the user activates this widget.
    # Later this will open the running applications menu
    # or switch between active applications/workbenches.
    activated = pyqtSignal()

    def __init__(self, maaya):

        super().__init__(maaya, show_border=False)

        self.maaya = maaya

        self.palette = self.maaya.theme.Palette

        self.spacing = self.maaya.theme.Spacing

        self.typography = self.maaya.typography()

        self.build_ui()

    def build_ui(self):

        # Placeholder runtime information.
        # Later this will display the currently focused
        # application and the number of running applications.
        self.runtime = QLabel(
            "Home • 0"
        )

        self.runtime.setFont(
            QFont(
                self.maaya.font["family"],
                self.typography.BODY_SIZE
            )
        )

        self.runtime.setStyleSheet(
            f"color: {self.palette.PRIMARY};"
        )

        self.runtime.setAlignment(
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
            self.runtime
        )

        self.setLayout(
            layout
        )

        self.set_inactive()

    def update_runtime(
        self,
        location: str,
        running_apps: int
    ):
        """
        Update the runtime information displayed in the header.
        """

        self.runtime.setText(
            f"{location} • {running_apps}"
        )

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