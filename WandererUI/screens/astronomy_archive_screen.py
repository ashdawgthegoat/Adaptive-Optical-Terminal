from services.eidolon import Eidolon

from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout
)

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class AstronomyArchiveScreen(QWidget):
    def __init__(self, return_callback, enter_callback):
        super().__init__()
        
        self.enter_callback = enter_callback
        self.return_callback = return_callback

        self.current_selection = 0
        self.item_labels = []

        self.setFocusPolicy(
            Qt.FocusPolicy.StrongFocus
        )

        layout = QVBoxLayout()
        layout.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        title = QLabel(
            "ASTRONOMY ARCHIVE"
        )

        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        title_font = QFont(
            "Monospace",
            24,
            QFont.Weight.Bold
        )

        title.setFont(title_font)
        title.setStyleSheet(
            "color: white;"
        )

        layout.addWidget(title)
        layout.addSpacing(40)

        self.menu_layout = layout

        footer = QLabel(
            "[ ESC ] Return"
        )

        footer.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        footer.setStyleSheet(
            "color: gray;"
        )

        self.footer = footer

        layout.addSpacing(40)
        layout.addWidget(footer)

        self.setLayout(layout)

        self.load_observations()

    def load_observations(self):

        self.observations = []

        self.current_selection = 0

        for label in self.item_labels:
            label.deleteLater()

        self.item_labels.clear()

        self.observations = (
            Eidolon.get_observations(
                "Astronomy"
            )
        )

        menu_font = QFont(
            "Monospace",
            16
        )

        for name in self.observations:

            label = QLabel()

            label.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            label.setFont(menu_font)

            self.item_labels.append(label)

            self.menu_layout.insertWidget(
                self.menu_layout.count() - 2,
                label
            )

        self.update_menu()

    def update_menu(self):

        if not self.observations:
            return

        for i, label in enumerate(
            self.item_labels
        ):

            if i == self.current_selection:

                label.setText(
                    f"▶ {self.observations[i]}"
                )

                label.setStyleSheet(
                    "color: white;"
                )

            else:

                label.setText(
                    f"  {self.observations[i]}"
                )

                label.setStyleSheet(
                    "color: gray;"
                )

    def keyPressEvent(self, event):

        if not self.observations:
            return

        if event.key() == Qt.Key.Key_Up:

            self.current_selection = (
                self.current_selection - 1
            ) % len(self.observations)

            self.update_menu()

        elif event.key() == Qt.Key.Key_Down:

            self.current_selection = (
                self.current_selection + 1
            ) % len(self.observations)

            self.update_menu()
        
        elif event.key() in (
            Qt.Key.Key_Return,
            Qt.Key.Key_Enter
        ):

            if self.enter_callback:

                observation_name = (
                    self.observations[
                        self.current_selection
                    ]
                )

                self.enter_callback(observation_name)

        elif event.key() == Qt.Key.Key_Escape:

            self.return_callback()

        else:

            super().keyPressEvent(event)        