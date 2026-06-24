from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class ArchiveScreen(QWidget):
    def __init__(self, return_callback):
        super().__init__()

        self.return_callback = return_callback

        self.menu_items = [
            "Astronomy",
            "Astrophotography",
            "Wildlife",
            "Spectroscopy",
            "Radio Astronomy"
        ]

        self.current_selection = 0
        self.item_labels = []

        self.setFocusPolicy(
            Qt.FocusPolicy.StrongFocus
        )

        layout = QVBoxLayout()
        layout.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        title = QLabel("ARCHIVE")
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

        layout.addWidget(title)
        layout.addSpacing(40)

        menu_font = QFont(
            "Monospace",
            16
        )

        for _ in self.menu_items:

            label = QLabel()

            label.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            label.setFont(menu_font)

            self.item_labels.append(label)

            layout.addWidget(label)

        footer = QLabel(
            "[ ESC ] Return"
        )

        footer.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        footer.setStyleSheet(
            "color: gray;"
        )

        layout.addSpacing(40)
        layout.addWidget(footer)

        self.setLayout(layout)

        self.update_menu()

        self.enter_callback = None

    def update_menu(self):

        for i, label in enumerate(
            self.item_labels
        ):

            if i == self.current_selection:

                label.setText(
                    f"▶ {self.menu_items[i]}"
                )

                label.setStyleSheet(
                    "color: white;"
                )

            else:

                label.setText(
                    f"  {self.menu_items[i]}"
                )

                label.setStyleSheet(
                    "color: gray;"
                )

    def keyPressEvent(self, event):

        if event.key() == Qt.Key.Key_Up:

            self.current_selection = (
                self.current_selection - 1
            ) % len(self.menu_items)

            self.update_menu()

        elif event.key() == Qt.Key.Key_Down:

            self.current_selection = (
                self.current_selection + 1
            ) % len(self.menu_items)

            self.update_menu()

        elif event.key() in (
            Qt.Key.Key_Return,
            Qt.Key.Key_Enter
        ):

            if self.enter_callback:

                self.enter_callback(
                    self.menu_items[
                        self.current_selection
                    ]
                )

        elif event.key() == Qt.Key.Key_Escape:

            self.return_callback()

        else:

            super().keyPressEvent(event)