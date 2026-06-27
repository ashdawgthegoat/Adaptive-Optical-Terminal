from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFrame
)

from widgets.header import Header
from widgets.footer import Footer
from widgets.navigation_panel import NavigationPanel
from widgets.viewport import Viewport
from widgets.context_panel import ContextPanel
from widgets.theme import (
    OUTER_MARGIN,
    INNER_MARGIN,
    SECTION_SPACING,
)
from widgets.separator import Separator

class MainLayout(QWidget):

    def __init__(self):
        super().__init__()

        self.header = Header()

        self.navigation = NavigationPanel()

        self.viewport = Viewport()

        self.context = ContextPanel()

        self.footer = Footer()

        self.build_ui()

    def build_ui(self):

        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(
            OUTER_MARGIN,
            OUTER_MARGIN,
            OUTER_MARGIN,
            OUTER_MARGIN
        )

        main_layout.setSpacing(
            SECTION_SPACING
        )

        body_layout = QHBoxLayout()

        body_layout.setContentsMargins(
            INNER_MARGIN,
            0,
            INNER_MARGIN,
            0
        )

        main_layout.addWidget(self.header)

        main_layout.addWidget(Separator())

        body_layout.addWidget(self.navigation,2)

        body_layout.addWidget(Separator(vertical=True))

        body_layout.addWidget(self.viewport,6)

        body_layout.addWidget(Separator(vertical=True))

        body_layout.addWidget(self.context,2)

        main_layout.addLayout(body_layout, stretch=1)

        main_layout.addWidget(Separator())

        main_layout.addWidget(self.footer)

        main_layout.addSpacing(INNER_MARGIN)

        self.setLayout(main_layout)

    def set_navigation(self,items):

        self.navigation.set_items(items)
