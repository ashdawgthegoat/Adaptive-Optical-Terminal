from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QHBoxLayout
)

from PyQt6.QtCore import (
    Qt,
    pyqtSignal
)

from PyQt6.QtGui import QFont


class NavigationItem(QFrame):

    clicked = pyqtSignal()

    def __init__(
        self,
        maaya,
        application,
    ):

        super().__init__()

        self.maaya = maaya

        self.palette = self.maaya.theme.Palette

        self.typography = self.maaya.typography()

        self.entry = application

        self.selected = False

        self.build_ui()

    def build_ui(self):

        self.setFixedHeight(56)

        self.layout = QHBoxLayout()

        self.layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        self.layout.setSpacing(0)

        self.setLayout(
            self.layout
        )

        self.accent = QFrame()

        self.accent.setFixedWidth(2)

        self.accent.setStyleSheet(
            f"background-color: {self.palette.ACCENT};"
        )

        self.label = QLabel(
            self.display_name()
        )

        self.label.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents
        )

        self.label.setFont(
            QFont(
                self.maaya.font["family"],
                self.typography.SECTION_SIZE
            )
        )

        self.label.setAlignment(
            Qt.AlignmentFlag.AlignVCenter
            |
            Qt.AlignmentFlag.AlignLeft
        )

        self.layout.addWidget(
            self.accent
        )

        self.layout.addSpacing(12)

        self.layout.addWidget(
            self.label
        )

        self.layout.addStretch()

        self.update_style()

    def display_name(self):

        if isinstance(self.entry, dict):

            return self.entry["name"]

        return self.entry

    def set_selected(
        self,
        selected
    ):

        self.selected = selected

        self.update_style()

    def update_style(self):

        if self.selected:

            self.label.setText(
                f">  {self.display_name()}"
            )

            self.setStyleSheet(
                f"""
                QFrame {{
                    background-color: {self.palette.SURFACE};
                }}

                QLabel {{
                    color: {self.palette.PRIMARY};
                    padding-left: 6px;
                }}
                """
            )

        else:

            self.label.setText(
                f"   {self.display_name()}"
            )

            self.setStyleSheet(
                f"""
                QFrame {{
                    background: transparent;
                }}

                QLabel {{
                    color: {self.palette.SECONDARY};
                    padding-left: 6px;
                }}
                """
            )
    
    def refresh_presentation(self):

        self.palette = self.maaya.theme.Palette

        self.typography = self.maaya.typography()

        self.label.setFont(
            QFont(
                self.maaya.font["family"],
                self.typography.SECTION_SIZE
            )
        )

        self.accent.setStyleSheet(
            f"background-color: {self.palette.ACCENT};"
        )

        self.update_style()

        self.update()

    def application_id(self):

        if isinstance(self.entry, dict):

            return self.entry["id"]

        return None

    def mousePressEvent(
        self,
        event
    ):

        if event.button() == Qt.MouseButton.LeftButton:

            self.clicked.emit()

        super().mousePressEvent(
            event
        )