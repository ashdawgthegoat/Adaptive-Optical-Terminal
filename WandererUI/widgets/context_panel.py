from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout
)

from PyQt6.QtCore import Qt
from widgets.theme import (
    PRIMARY,
    ITEM_SPACING,
    SECTION_FONT,
    SMALL_FONT,
    SECONDARY
)

class ContextPanel(QWidget):

    def __init__(
        self,
        title="SYSTEM STATUS"
    ):
        super().__init__()

        self.title = QLabel(title)

        self.info_labels = []

        self.build_ui()

    def build_ui(self):

        self.layout = QVBoxLayout()

        self.layout.setContentsMargins(0, 0, 0, 0)

        self.layout.setAlignment(
            Qt.AlignmentFlag.AlignTop
        )

        self.layout.setSpacing(ITEM_SPACING)

        self.title.setFont(
            SECTION_FONT
        )

        self.title.setStyleSheet(
            f"color: {PRIMARY};"
        )

        self.layout.addWidget(
            self.title
        )

        self.layout.addSpacing(ITEM_SPACING)

        self.setLayout(
            self.layout
        )

    def set_info(self,info):

        for label in self.info_labels:
            label.deleteLater()

        self.info_labels.clear()

        for key, value in info.items():

            label = QLabel(
                f"{key}\n{value}"
            )

            label.setFont(
                SMALL_FONT
            )

            label.setStyleSheet(
                f"color: {SECONDARY};"
            )

            self.layout.addWidget(
                label
            )

            self.info_labels.append(
                label
            )

    def set_title(self,title):

        self.title.setText(
            title
        )