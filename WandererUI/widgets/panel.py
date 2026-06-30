from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import (
    pyqtSignal,
    Qt
)


class Panel(QFrame):

    clicked = pyqtSignal()

    def __init__(
        self,
        maaya
    ):

        super().__init__()

        self.maaya = maaya

        self.palette = self.maaya.theme.Palette

        self.borders = self.maaya.theme.Borders

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
                    border: {self.borders.ACTIVE_WIDTH}px solid {self.palette.ACCENT};
                }}
                """
            )

        else:

            self.setStyleSheet(
                f"""
                QFrame#panel {{
                    border: {self.borders.WIDTH}px solid {self.palette.SEPARATOR};
                }}
                """
            )

    # =========================================

    def mousePressEvent(self, event):

        if event.button() == Qt.MouseButton.LeftButton:

            self.clicked.emit()

        super().mousePressEvent(event)