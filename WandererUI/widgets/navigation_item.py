from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QHBoxLayout
)

from PyQt6.QtCore import (Qt, pyqtSignal)

from widgets.theme import (
    SECTION_FONT,
    PRIMARY,
    SECONDARY,
    ACCENT,
    SURFACE
)


class NavigationItem(QFrame):

    clicked = pyqtSignal()

    def __init__(self, text):
        super().__init__()

        self.text = text
        self.selected = False

        self.build_ui()

    def build_ui(self):

        self.setFixedHeight(56)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.setLayout(self.layout)

        # Permanent left accent line
        self.accent = QFrame()
        self.accent.setFixedWidth(2)
        self.accent.setStyleSheet(
            f"background-color: {ACCENT};"
        )

        # Menu text
        self.label = QLabel(self.text)
        self.label.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents
        )
        self.label.setFont(SECTION_FONT)
        self.label.setAlignment(
            Qt.AlignmentFlag.AlignVCenter |
            Qt.AlignmentFlag.AlignLeft
        )

        self.layout.addWidget(self.accent)
        self.layout.addSpacing(12)
        self.layout.addWidget(self.label)
        self.layout.addStretch()

        self.update_style()

    def set_selected(self, selected):

        self.selected = selected
        self.update_style()

    def update_style(self):

        if self.selected:

            self.label.setText(f">  {self.text}")

            self.setStyleSheet(
                f"""
                QFrame {{
                    background-color: {SURFACE};
                }}

                QLabel {{
                    color: {PRIMARY};
                    padding-left: 6px;
                }}
                """
            )

        else:

            self.label.setText(f"   {self.text}")

            self.setStyleSheet(
                f"""
                QFrame {{
                    background: transparent;
                }}

                QLabel {{
                    color: {SECONDARY};
                    padding-left: 6px;
                }}
                """
            )

    def mousePressEvent(self, event):

        if event.button() == Qt.MouseButton.LeftButton:

            self.clicked.emit()

        super().mousePressEvent(event)