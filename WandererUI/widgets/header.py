from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout
)

from PyQt6.QtCore import Qt
from widgets.theme import (
    TITLE_FONT,
    BODY_FONT,
    PRIMARY,
    ACCENT,
    ITEM_SPACING
)


class Header(QWidget):

    def __init__(
        self,
        title="WANDERER",
        subtitle="MK II Alpha"
    ):
        super().__init__()

        self.title = QLabel(title)
        self.subtitle = QLabel(subtitle)

        self.build_ui()

    def build_ui(self):

        self.title.setFont(TITLE_FONT)
        self.subtitle.setFont(BODY_FONT)

        self.title.setStyleSheet(
            f"color: {PRIMARY};"
        )

        self.subtitle.setStyleSheet(
            f"color: {ACCENT};"
        )

        left_layout = QVBoxLayout()

        left_layout.setSpacing(ITEM_SPACING // 2)

        left_layout.addWidget(
            self.title
        )

        left_layout.addWidget(
            self.subtitle
        )

        main_layout = QHBoxLayout()

        main_layout.addLayout(
            left_layout
        )

        main_layout.addStretch()

        self.setLayout(
            main_layout
        )

    def set_title(self,title,subtitle=None):

        self.title.setText(title)

        if subtitle is not None:
            self.subtitle.setText(
                subtitle
            )