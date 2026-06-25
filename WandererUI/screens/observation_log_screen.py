from services.eidolon import Eidolon

from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout
)

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class ObservationLogScreen(QWidget):
    def __init__(self, return_callback):
        super().__init__()

        self.return_callback = return_callback

        self.setFocusPolicy(
            Qt.FocusPolicy.StrongFocus
        )

        layout = QVBoxLayout()
        layout.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.title = QLabel(
            "OBSERVATION LOG"
        )

        self.title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        title_font = QFont(
            "Monospace",
            24,
            QFont.Weight.Bold
        )

        self.title.setFont(title_font)
        self.title.setStyleSheet(
            "color: white;"
        )

        self.content = QLabel()

        self.content.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.content.setStyleSheet(
            "color: white;"
        )

        footer = QLabel(
            "[ ESC ] Return"
        )

        footer.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        footer.setStyleSheet(
            "color: gray;"
        )

        layout.addWidget(self.title)
        layout.addSpacing(30)
        layout.addWidget(self.content)
        layout.addSpacing(30)
        layout.addWidget(footer)

        self.setLayout(layout)

    def load_observation(
        self,
        observation_name
    ):

        observation = (
            Eidolon.open_observation(
                "Astronomy",
                observation_name
            )
        )

        if observation is None:

            self.content.setText(
                "Observation not found."
            )

            return

        self.content.setText(
            f"""
Name:
{observation['name']}

Category:
{observation['category']}

Notes:
{observation['notes']}
"""
        )

    def keyPressEvent(self, event):

        if event.key() == Qt.Key.Key_Escape:

            self.return_callback()

        else:

            super().keyPressEvent(event)