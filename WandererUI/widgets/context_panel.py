from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QWidget,
    QVBoxLayout,
    QScrollArea
)

from PyQt6.QtCore import Qt

from widgets.theme import (
    PRIMARY,
    SECTION_FONT,
    ACCENT
)

from widgets.info_cell import InfoCell
from widgets.panel import Panel


class ContextPanel(Panel):

    def __init__(self):

        super().__init__()

        self.build_ui()

    # =====================================

    def build_ui(self):

        root_layout = QVBoxLayout()

        self.scroll = QScrollArea()

        self.content = QWidget()

        self.main_layout = QVBoxLayout()

        self.main_layout.setContentsMargins(
            10,
            10,
            10,
            10
        )

        self.main_layout.setSpacing(8)

        # ============================
        # SYSTEM SECTION
        # ============================

        self.system_title = QLabel(
            "SYSTEM STATUS"
        )

        self.system_title.setFont(
            SECTION_FONT
        )

        self.system_title.setStyleSheet(
            f"color: {PRIMARY};"
        )

        self.system_title.setAlignment(
            Qt.AlignmentFlag.AlignLeft
        )

        self.main_layout.addWidget(
            self.system_title
        )

        self.system_layout = QVBoxLayout()

        self.system_layout.setSpacing(4)

        self.main_layout.addLayout(
            self.system_layout,
            3
        )

        # ============================
        # DIVIDER
        # ============================

        divider = QFrame()

        divider.setFrameShape(
            QFrame.Shape.HLine
        )

        divider.setFixedHeight(1)

        divider.setStyleSheet(
            f"""
            background-color: {ACCENT};
            """
        )

        self.main_layout.addWidget(
            divider
        )

        # ============================
        # MODULE PORT
        # ============================

        self.module_title = QLabel(
            "MODULE PORT"
        )

        self.module_title.setFont(
            SECTION_FONT
        )

        self.module_title.setStyleSheet(
            f"color: {PRIMARY};"
        )

        self.main_layout.addWidget(
            self.module_title
        )

        self.module_layout = QVBoxLayout()

        self.module_layout.setSpacing(4)

        self.main_layout.addLayout(
            self.module_layout,
            1
        )

        self.content.setLayout(
            self.main_layout
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

        self.scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        root_layout.addWidget(
            self.scroll
        )

        self.setLayout(
            root_layout
        )

        self.set_module_info({
            "Status": "No Active Module"
        })

        self.set_inactive()

    # =====================================

    def _clear_layout(self, layout):

        while layout.count():

            item = layout.takeAt(0)

            if item.widget():

                item.widget().deleteLater()

    # =====================================

    def set_info(self, info):

        self._clear_layout(
            self.system_layout
        )

        for key, value in info.items():

            cell = InfoCell(
                title=key,
                value=value
            )

            self.system_layout.addWidget(
                cell
            )

        self.system_layout.addStretch()

    # =====================================

    def set_module_info(self, info):

        self._clear_layout(
            self.module_layout
        )

        for key, value in info.items():

            cell = InfoCell(
                title=key,
                value=value
            )

            self.module_layout.addWidget(
                cell
            )

        self.module_layout.addStretch()

    # =====================================

    def set_title(self, title):

        self.system_title.setText(
            title
        )

    # =====================================

    def clear_module(self):

        self.set_module_info({

            "Status": "No Active Module"

        })