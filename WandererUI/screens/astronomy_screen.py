from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class AstronomyScreen(QWidget):
    def __init__(self, return_callback):
        super().__init__()

        self.return_callback = return_callback
        self.menu_items = [
            "New Observation",
            "Sky Atlas",
            "Telescope Control",
            "Star Database"
        ]

        self.current_selection = 0
        self.item_labels = []

        self.enter_callback = None

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("ASTRONOMY")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_font = QFont("Monospace", 32, QFont.Weight.Bold)
        title_font.setStyleHint(QFont.StyleHint.TypeWriter)

        title.setFont(title_font)
        title.setStyleSheet("color: white;")

        menu_font = QFont("Monospace", 16)
        menu_font.setStyleHint(QFont.StyleHint.TypeWriter)

        layout.addWidget(title)
        layout.addSpacing(40)

        for _ in self.menu_items:
            item_label = QLabel()
            item_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            item_label.setFont(menu_font)

            self.item_labels.append(item_label)

            layout.addWidget(item_label)
            layout.addSpacing(10)

        footer = QLabel("[ ESC ] Return")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("color: gray;")

        layout.addSpacing(40)
        layout.addWidget(footer)

        self.setLayout(layout)
        self.update_menu()
    
    def update_menu(self):
        for i, label in enumerate(self.item_labels):

            if i == self.current_selection:
                label.setText(f"▶ {self.menu_items[i]}")
                label.setStyleSheet("color: white;")
            else:
                label.setText(f"  {self.menu_items[i]}")
                label.setStyleSheet("color: gray;")

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
                    self.menu_items[self.current_selection]
                )

        elif event.key() == Qt.Key.Key_Escape:
            self.return_callback()

        else:
            super().keyPressEvent(event)