from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout
)

from PyQt6.QtCore import Qt

from widgets.theme import (
    PRIMARY,
    SECONDARY,
    SECTION_FONT,
    SMALL_FONT
)


class ContextPanel(QWidget):

    def __init__(self, title="SYSTEM STATUS"):
        super().__init__()

        self.title = QLabel(title)

        self.info = {}

        self.build_ui()

    def build_ui(self):

        self.layout = QVBoxLayout()

        self.layout.setContentsMargins(
            10,
            10,
            10,
            10
        )

        self.layout.setSpacing(0)

        self.setLayout(self.layout)

        self.title.setFont(SECTION_FONT)

        self.title.setStyleSheet(
            f"color: {PRIMARY};"
        )

        self.title.setAlignment(
            Qt.AlignmentFlag.AlignLeft
        )

        self.layout.addWidget(self.title)

    def set_info(self, info):

        self.info = info

        while self.layout.count() > 1:

            item = self.layout.takeAt(1)

            if item.widget():
                item.widget().deleteLater()

        for key, value in info.items():

            cell = QWidget()

            cell_layout = QVBoxLayout()

            cell_layout.setContentsMargins(
                0,
                0,
                0,
                0
            )

            cell_layout.setSpacing(2)

            key_label = QLabel(key)

            key_label.setFont(SMALL_FONT)

            key_label.setStyleSheet(
                f"color: {PRIMARY};"
            )

            value_label = QLabel(str(value))

            value_label.setFont(SMALL_FONT)

            value_label.setStyleSheet(
                f"color: {SECONDARY};"
            )

            cell_layout.addWidget(key_label)

            cell_layout.addWidget(value_label)

            cell.setLayout(cell_layout)

            self.layout.addWidget(
                cell,
                1
            )

    def set_title(self, title):

        self.title.setText(title)