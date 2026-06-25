from services.eidolon import Eidolon
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QLineEdit
)

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont


class NewObservationScreen(QWidget):
    def __init__(self, return_callback):
        super().__init__()

        self.category = "Astronomy"

        self.category_label = QLabel()

        self.return_callback = return_callback

        layout = QVBoxLayout()
        layout.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        title = QLabel("NEW OBSERVATION")
        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        title_font = QFont(
            "Monospace",
            32,
            QFont.Weight.Bold
        )

        title.setFont(title_font)
        title.setStyleSheet(
            "color: white;"
        )

        self.category_label.setText(
            f"Category: {self.category}"
        )

        self.category_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.category_label.setStyleSheet(
            "color: gray;"
        )

        self.name_input = QLineEdit()

        self.name_input.setPlaceholderText(
            "Observation Name"
        )

        self.name_input.setFixedWidth(300)

        footer = QLabel(
            "[ ENTER ] Create    [ ESC ] Cancel"
        )

        footer.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        footer.setStyleSheet(
            "color: gray;"
        )

        layout.addWidget(title)
        layout.addSpacing(20)

        layout.addWidget(self.category_label)
        layout.addSpacing(20)

        layout.addWidget(self.name_input,alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(30)

        layout.addWidget(footer)

        self.setLayout(layout)

    def showEvent(self, event):
        super().showEvent(event)

        QTimer.singleShot(
            100,
            self.name_input.setFocus
        )
    
    def save_observation(self):

        name = (
            self.name_input
            .text()
            .strip()
        )

        if not name:
            return

        success = (
            Eidolon.create_observation(
                self.category,
                name
            )
        )

        if success:

            print(
                f"Created observation: {name}"
            )

            self.name_input.clear()
            self.name_input.setFocus()

        else:

            print(
                f"Observation already exists: {name}"
            )

    def keyPressEvent(self, event):

        if event.key() == Qt.Key.Key_Escape:
            self.return_callback()

        elif event.key() in (
            Qt.Key.Key_Return,
            Qt.Key.Key_Enter
        ):

           self.save_observation()

        else:
            super().keyPressEvent(event)

    def set_category(self,category):

        self.category = category

        self.category_label.setText(
            f"Category: {category}"
        )