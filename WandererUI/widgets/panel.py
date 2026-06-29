from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import (
    pyqtSignal,
    Qt
)

from widgets.theme import (
    ACCENT
)


class Panel(QFrame):

    clicked =pyqtSignal()

    def __init__(self):

        super().__init__()

        self.active = False

        self.setObjectName("panel")

        self.refresh_style()

    # =========================================

    def set_active(self):

        self.active = True

        self.refresh_style()

    # =========================================

    def set_inactive(self):

        self.active = False

        self.refresh_style()

    # =========================================

    def is_active(self):

        return self.active

    # =========================================

    def refresh_style(self):

        if self.active:

            self.setStyleSheet(
                f"""
                QFrame#panel {{
                    border: 1px solid {ACCENT};
                }}
                """
            )

        else:

            self.setStyleSheet(
                """
                QFrame#panel {
                    border: 1px solid #303030;
                }
                """
            )

    def mousePressEvent(self, event):

        if event.button() == Qt.MouseButton.LeftButton:

            self.clicked.emit()

        super().mousePressEvent(event)