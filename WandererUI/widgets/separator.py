from PyQt6.QtWidgets import QFrame

from widgets.theme import (
    SEPARATOR
)


class Separator(QFrame):

    def __init__(self, vertical=False):
        super().__init__()

        if vertical:
            self.setFrameShape(QFrame.Shape.VLine)
            self.setFixedWidth(1)
        else:
            self.setFrameShape(QFrame.Shape.HLine)
            self.setFixedHeight(1)

        self.setFrameShadow(QFrame.Shadow.Plain)

        self.setStyleSheet(
            f"""
            QFrame {{
                background-color: {SEPARATOR};
                color: {SEPARATOR};
            }}
            """
        )