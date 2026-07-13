from PyQt6.QtCore import Qt, pyqtSignal

from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
)

class Overlay(QWidget):

    item_selected = pyqtSignal(object)
    cancelled = pyqtSignal()

    def __init__(self):

        super().__init__()

        self.items = []
        self.index = 0

        self.build_ui()

        self.hide()

    def build_ui(self):

        self.setFixedSize(500, 350)

        self.title = QLabel()

        self.list = QLabel()

        layout = QVBoxLayout()

        layout.addWidget(self.title)
        layout.addWidget(self.list)

        self.setLayout(layout)

    def show_overlay(self, title, items):

        self.title.setText(title)

        self.items = items

        self.index = 0

        self.refresh()

        self.show()

    def hide_overlay(self):

        self.hide()

    def refresh(self):

        lines = []

        for i, item in enumerate(self.items):

            prefix = ">" if i == self.index else " "

            lines.append(f"{prefix} {item}")

        self.list.setText("\n".join(lines))

    def move_up(self):

        if not self.items:
            return

        self.index = max(0, self.index - 1)

        self.refresh()

    def move_down(self):

        if not self.items:
            return

        self.index = min(
            len(self.items) - 1,
            self.index + 1
        )

        self.refresh()

    def activate(self):

        if not self.items:
            return

        self.item_selected.emit(
            self.items[self.index]
        )

        self.hide_overlay()

    def cancel(self):

        self.cancelled.emit()

        self.hide_overlay()