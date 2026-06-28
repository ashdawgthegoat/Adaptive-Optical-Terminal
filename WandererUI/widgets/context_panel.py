from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QFrame
)

from PyQt6.QtCore import Qt

from widgets.theme import (
    PRIMARY,
    SECONDARY,
    SECTION_FONT,
    SMALL_FONT,
    ACCENT
)

from widgets.info_cell import InfoCell


class ContextPanel(QWidget):

    def __init__(self):

        super().__init__()

        self.build_ui()

    def build_ui(self):

        self.main_layout = QVBoxLayout()

        self.main_layout.setContentsMargins(
            10,
            10,
            10,
            10
        )

        self.main_layout.setSpacing(8)

        self.setLayout(
            self.main_layout
        )

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

        divider.setStyleSheet(
            f"""
            color: {ACCENT};
            background-color: {ACCENT};
            """
        )

        divider.setFixedHeight(1)

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

        self.set_module_info({
            "Status": "No Active Module"
        })

    # =====================================

    def _clear_layout(
        self,
        layout
    ):

        while layout.count():

            item = layout.takeAt(0)

            if item.widget():

                item.widget().deleteLater()

    # =====================================

    def set_info(self,info):

        self._clear_layout(
            self.system_layout
        )

        for key, value in info.items():

            self.system_layout.addWidget(

                InfoCell(

                    title=key,

                    value=value

                )

            )

            self.system_layout.addStretch()

    # =====================================

    def set_module_info(self,info):

        self._clear_layout(
            self.module_layout
        )

        for key, value in info.items():

            self.module_layout.addWidget(

                InfoCell(

                    title=key,

                    value=value

                )

            )

            self.module_layout.addStretch()

    # =====================================

    def set_title(
        self,
        title
    ):

        self.system_title.setText(
            title
        )
    
    def clear_module(self):

        self.set_module_info({

            "Status":
                "No Active Module"

        })