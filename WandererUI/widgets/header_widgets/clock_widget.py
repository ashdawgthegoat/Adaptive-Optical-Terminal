from PyQt6.QtWidgets import (
    QLabel,
    QHBoxLayout,
)

from PyQt6.QtCore import (
    Qt,
    pyqtSignal,
    QTimer,
    QDateTime,
)

from PyQt6.QtGui import QFont

from widgets.layer.panel import Panel


class ClockWidget(Panel):

    # Emitted when the user activates this widget.
    # Later this may open a calendar or agenda.
    activated = pyqtSignal()

    def __init__(self, maaya):

        super().__init__(maaya, show_border=False)

        self.maaya = maaya

        self.palette = self.maaya.theme.Palette

        self.spacing = self.maaya.theme.Spacing

        self.typography = self.maaya.typography()

        self.build_ui()

        self.timer = QTimer(self)

        self.timer.timeout.connect(
            self.update_time
        )

        self.timer.start(
            1000
        )

        self.update_time()

    def build_ui(self):

        self.clock = QLabel()

        self.clock.setFont(
            QFont(
                self.maaya.font["family"],
                self.typography.BODY_SIZE
            )
        )

        self.clock.setStyleSheet(
            f"color: {self.palette.PRIMARY};"
        )

        self.clock.setAlignment(
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
            self.clock
        )

        self.setLayout(
            layout
        )

        self.set_inactive()

    def refresh_presentation(self):

        self.palette = self.maaya.theme.Palette

        self.spacing = self.maaya.theme.Spacing

        self.typography = self.maaya.typography()

        self.clock.setFont(
            QFont(
                self.maaya.font["family"],
                self.typography.BODY_SIZE
            )
        )

        self.clock.setStyleSheet(
            f"color: {self.palette.PRIMARY};"
        )

        self.update()

    def update_time(self):

        current = QDateTime.currentDateTime()

        self.clock.setText(
            current.toString(
                "dd MMM yyyy  |  hh:mm:ss"
            )
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