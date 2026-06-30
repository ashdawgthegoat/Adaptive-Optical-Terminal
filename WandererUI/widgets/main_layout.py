from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
)

from widgets.header import Header
from widgets.footer import Footer
from widgets.navigation_panel import NavigationPanel
from widgets.viewport import Viewport
from widgets.context_panel import ContextPanel


class MainLayout(QWidget):

    def __init__(
        self,
        maaya
    ):

        super().__init__()

        self.maaya = maaya

        self.header = Header(
            self.maaya
        )

        self.navigation = NavigationPanel(
            self.maaya
        )

        self.viewport = Viewport(
            self.maaya
        )

        self.context = ContextPanel(
            self.maaya
        )

        self.footer = Footer(
            self.maaya
        )

        self.build_ui()

    def build_ui(self):

        spacing = self.maaya.theme.Spacing

        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(
            spacing.OUTER_MARGIN,
            spacing.OUTER_MARGIN,
            spacing.OUTER_MARGIN,
            spacing.OUTER_MARGIN
        )

        main_layout.setSpacing(
            spacing.SECTION_SPACING
        )

        body_layout = QHBoxLayout()

        body_layout.setSpacing(4)

        body_layout.setContentsMargins(
            spacing.INNER_MARGIN,
            0,
            spacing.INNER_MARGIN,
            0
        )

        header_layout = QHBoxLayout()

        header_layout.setContentsMargins(
            spacing.INNER_MARGIN,
            0,
            spacing.INNER_MARGIN,
            0
        )

        header_layout.addWidget(
            self.header
        )

        main_layout.addLayout(
            header_layout
        )

        body_layout.addWidget(
            self.navigation,
            2
        )

        body_layout.addWidget(
            self.viewport,
            6
        )

        body_layout.addWidget(
            self.context,
            2
        )

        main_layout.addLayout(
            body_layout,
            stretch=1
        )

        footer_layout = QHBoxLayout()

        footer_layout.setContentsMargins(
            spacing.INNER_MARGIN,
            0,
            spacing.INNER_MARGIN,
            0
        )

        footer_layout.addWidget(
            self.footer
        )

        main_layout.addLayout(
            footer_layout
        )

        self.setLayout(
            main_layout
        )

    def set_navigation(
        self,
        items
    ):

        self.navigation.set_items(
            items
        )