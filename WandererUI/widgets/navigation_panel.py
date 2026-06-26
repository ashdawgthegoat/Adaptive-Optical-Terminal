from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout
)

from PyQt6.QtCore import Qt
from widgets.theme import (
    SECTION_FONT,
    PRIMARY,
    SECONDARY,
    ITEM_SPACING
)


class NavigationPanel(QWidget):

    def __init__(self, items=None):
        super().__init__()

        self.items = items or []

        self.current_selection = 0

        self.labels = []

        self.build_ui()

    def build_ui(self):

        self.layout = QVBoxLayout()

        self.layout.setContentsMargins(0, 0, 0, 0)

        self.layout.setAlignment(
            Qt.AlignmentFlag.AlignTop
        )

        self.layout.setSpacing(ITEM_SPACING)

        self.setLayout(
            self.layout
        )

        self.set_items(
            self.items
        )

    def set_items(self,items):

        self.items = items

        self.current_selection = 0

        for label in self.labels:
            label.deleteLater()

        self.labels.clear()

        for item in self.items:

            label = QLabel()

            label.setFont(
                SECTION_FONT
            )

            label.setAlignment(
                Qt.AlignmentFlag.AlignLeft
            )

            self.layout.addWidget(
                label
            )

            self.labels.append(
                label
            )

        self.update_selection()

    def update_selection(self):

        for i, label in enumerate(
            self.labels
        ):

            if i == self.current_selection:

                label.setText(
                    f"▶ {self.items[i]}"
                )

                label.setStyleSheet(
                    f"color: {PRIMARY};"
                )

            else:

                label.setText(
                    f"  {self.items[i]}"
                )

                label.setStyleSheet(
                    f"color: {SECONDARY};"
                )
    
    def move_up(self):

        if not self.items:
            return

        self.current_selection = (
            self.current_selection - 1
        ) % len(self.items)

        self.update_selection()

    def move_down(self):

        if not self.items:
            return

        self.current_selection = (
            self.current_selection + 1
        ) % len(self.items)

        self.update_selection()

    def current_item(self):

        if not self.items:
            return None

        return self.items[
            self.current_selection
        ]