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


class Header(Panel):

    left_requested = pyqtSignal()

    right_requested = pyqtSignal()

    up_requested = pyqtSignal()

    down_requested = pyqtSignal()

    activated = pyqtSignal()

    def __init__(
        self,
        maaya,
        title="WANDERER",
        subtitle="MK II Alpha"
    ):

        super().__init__(maaya)

        self.maaya = maaya

        self.palette = self.maaya.theme.Palette

        self.spacing = self.maaya.theme.Spacing

        self.typography = self.maaya.typography()

        self.title = QLabel(title)

        self.subtitle = QLabel(subtitle)

        self.build_ui()

    def build_ui(self):

        self.title.setFont(
            QFont(
                self.maaya.font["family"],
                self.typography.TITLE_SIZE
            )
        )

        self.subtitle.setFont(
            QFont(
                self.maaya.font["family"],
                self.typography.BODY_SIZE
            )
        )

        self.title.setStyleSheet(
            f"color: {self.palette.PRIMARY};"
        )

        self.subtitle.setStyleSheet(
            f"color: {self.palette.ACCENT};"
        )

        self.title.setAlignment(
            Qt.AlignmentFlag.AlignLeft
        )

        title_layout = QHBoxLayout()

        title_layout.setSpacing(
            self.spacing.ITEM_SPACING
        )

        title_layout.addWidget(
            self.title
        )

        title_layout.addWidget(
            self.subtitle
        )

        title_layout.addStretch()

        main_layout = QHBoxLayout()

        main_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        main_layout.addLayout(
            title_layout
        )

        main_layout.setAlignment(
            title_layout,
            Qt.AlignmentFlag.AlignVCenter
        )

        self.setLayout(
            main_layout
        )

        self.set_inactive()

    def set_title(
        self,
        title,
        subtitle=None
    ):

        self.title.setText(
            title
        )

        self.subtitle.setAlignment(
            Qt.AlignmentFlag.AlignVCenter
        )

        if subtitle is not None:

            self.subtitle.setText(
                subtitle
            )

        self.subtitle.setStyleSheet(
            f"color: {self.palette.ACCENT};"
        )

    def keyPressEvent(
        self,
        event
    ):

        match event.key():

            case Qt.Key.Key_Left:
                self.left_requested.emit()

            case Qt.Key.Key_Right:
                self.right_requested.emit()

            case Qt.Key.Key_Up:
                self.up_requested.emit()

            case Qt.Key.Key_Down:
                self.down_requested.emit()

            case Qt.Key.Key_Return | Qt.Key.Key_Enter:
                self.activated.emit()

            case _:
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