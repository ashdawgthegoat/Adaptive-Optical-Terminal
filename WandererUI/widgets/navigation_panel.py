from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout
)

from PyQt6.QtCore import Qt

from widgets.theme import (
    SECTION_FONT,
    PRIMARY
)

from widgets.navigation_item import NavigationItem


class NavigationPanel(QWidget):

    def __init__(self, items=None):
        super().__init__()

        self.title = QLabel("MAIN MENU")

        self.items = items or []

        self.current_selection = 0

        self.nav_items = []

        self.build_ui()

    def build_ui(self):

        self.layout = QVBoxLayout()

        self.layout.setContentsMargins(
            10,
            10,
            10,
            10
        )

        self.layout.setSpacing(12)

        self.layout.setAlignment(
            Qt.AlignmentFlag.AlignTop
        )

        self.setLayout(self.layout)

        self.title.setFont(SECTION_FONT)

        self.title.setStyleSheet(
            f"color: {PRIMARY};"
        )

        self.title.setAlignment(
            Qt.AlignmentFlag.AlignLeft
        )

        self.layout.addWidget(self.title)

        self.layout.addSpacing(8)

        self.set_items(self.items)

        self.layout.addStretch()

    def set_items(self, items):

        self.items = items

        self.current_selection = 0

        for item in self.nav_items:
            item.deleteLater()

        self.nav_items.clear()

        for text in self.items:

            item = NavigationItem(text)

            self.layout.addWidget(item)

            self.nav_items.append(item)

            self.layout.addStretch()

        self.update_selection()

    def update_selection(self):

        for i, item in enumerate(self.nav_items):

            item.set_selected(
                i == self.current_selection
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