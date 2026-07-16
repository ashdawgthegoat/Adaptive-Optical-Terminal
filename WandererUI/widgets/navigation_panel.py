from PyQt6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QScrollArea,
    QWidget
)

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from widgets.navigation_widgets.navigation_item import NavigationItem
from widgets.layer.panel import Panel

# ==========================================================
# Navigation Panel
#
# Displays the primary navigation options of WandererUI.
# This panel participates in the focus system and renders
# the standard panel border.
# ==========================================================

class NavigationPanel(Panel):

    activated = pyqtSignal(object)

    def __init__(
        self,
        maaya,
    ):

        super().__init__(
            maaya,
            show_border=True
        )

        self.maaya = maaya

        self.palette = self.maaya.theme.Palette
        self.spacing = self.maaya.theme.Spacing
        self.typography = self.maaya.typography()

        self.title = QLabel()

        self.items = []

        self.current_selection = 0

        self.nav_items = []

        self.build_ui()

    # ==========================================================
    # UI Construction
    # ==========================================================

    def build_ui(self):

        self.set_title("MAIN MENU")

        self.layout = QVBoxLayout()

        padding = self.content_padding()

        self.layout.setContentsMargins(
            padding,    
            padding,
            padding,
            padding
        )

        self.scroll = QScrollArea()

        self.content = QWidget()

        self.content_layout = QVBoxLayout()

        self.content_layout.setContentsMargins(
            10,
            10,
            10,
            10
        )

        self.content_layout.setSpacing(
            self.spacing.ITEM_SPACING
        )

        self.content_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop
        )

        self.title.setFont(
            QFont(
                self.maaya.font["family"],
                self.typography.SECTION_SIZE
            )
        )

        self.title.setStyleSheet(
            f"color: {self.palette.PRIMARY};"
        )

        self.title.setAlignment(
            Qt.AlignmentFlag.AlignLeft
        )

        self.content_layout.addWidget(
            self.title
        )

        self.content_layout.addSpacing(
            8
        )

        self.set_items([])

        self.content.setLayout(
            self.content_layout
        )

        self.scroll.setWidget(
            self.content
        )

        self.scroll.setWidgetResizable(
            True
        )

        self.scroll.setFrameShape(
            QScrollArea.Shape.NoFrame
        )

        self.scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.layout.addWidget(
            self.scroll
        )

        self.setLayout(
            self.layout
        )

        self.set_inactive()

    def set_title(self, title):

        self.title.setText(title)

    # ==========================================================
    # Navigation Item Management
    # ==========================================================

    def set_items(
        self,
        items
    ):

        self.items = items

        self.current_selection = 0

        for item in self.nav_items:

            item.deleteLater()

        self.nav_items.clear()

        for entry in self.items:

            item = NavigationItem(
                self.maaya,
                entry
            )

            item.clicked.connect(
                lambda checked=False, i=len(self.nav_items):
                self.select_item(i)
            )

            self.content_layout.addWidget(
                item
            )

            self.nav_items.append(
                item
            )

        self.update_selection()

    # ==========================================================
    # Selection Management
    # ==========================================================

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

    def select_item(
        self,
        index
    ):

        if 0 <= index < len(self.items):

            self.current_selection = index

            self.update_selection()

    # ==========================================================
    # Activation
    # ==========================================================

    def activate(self):
        """Activate the currently selected entry."""

        print("[1] activate()")

        item = self.current_item()

        if item is None:
            return

        self.activated.emit(item)

    # ==========================================================
    # Refresh
    # ==========================================================

    def refresh_presentation(self):

        self.palette = self.maaya.theme.Palette

        self.spacing = self.maaya.theme.Spacing

        self.typography = self.maaya.typography()

        self.title.setFont(
            QFont(
                self.maaya.font["family"],
                self.typography.SECTION_SIZE
            )
        )

        self.title.setStyleSheet(
            f"color: {self.palette.PRIMARY};"
        )

        self.content_layout.setSpacing(
            self.spacing.ITEM_SPACING
        )

        for item in self.nav_items:

            item.refresh_presentation()

        self.update()

    # ==========================================================
    # Cleanup
    # ==========================================================

    def clear_items(self):

        while self.content_layout.count():

            item = self.content_layout.takeAt(0)

            if item.widget():

                item.widget().deleteLater()