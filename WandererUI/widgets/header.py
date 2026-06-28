from PyQt6.QtWidgets import (
    QFrame,
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
    ITEM_SPACING,
    SUBTITLE_FONT
)

from widgets.panel import Panel

class Header(Panel):

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
        self.subtitle.setFont(SUBTITLE_FONT)

        self.title.setStyleSheet(
            f"color: {PRIMARY};"
        )

        self.subtitle.setStyleSheet(
            f"color: {ACCENT};"
        )

        self.title.setAlignment(
            Qt.AlignmentFlag.AlignLeft
        )

        title_layout = QHBoxLayout()

        title_layout.setSpacing(
            30
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

    def set_title(self,title,subtitle=None):

        self.title.setText(title)

        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        if subtitle is not None:
            self.subtitle.setText(
                subtitle
            )

        self.subtitle.setStyleSheet(
            f"""
            color: {ACCENT};
            """
        )