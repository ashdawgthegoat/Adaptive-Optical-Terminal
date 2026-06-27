from PyQt6.QtWidgets import QFrame

from widgets.theme import (
    SEPARATOR
)


class Separator(QFrame):

    def __init__(self):
        super().__init__()

        self.setFrameShape(
            QFrame.Shape.HLine
        )

        self.setFrameShadow(
            QFrame.Shadow.Plain
        )

        self.setStyleSheet(
            f"""
            QFrame {{
                color: {SEPARATOR};
                background-color: {SEPARATOR};
                min-height: 1px;
                max-height: 1px;
            }}
            """
        )