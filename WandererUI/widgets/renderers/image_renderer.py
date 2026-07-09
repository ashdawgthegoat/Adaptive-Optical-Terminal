from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from widgets.renderers.base_renderer import BaseRenderer

class ImageRenderer(BaseRenderer):

    def __init__(self, maaya):

        super().__init__()

        self.maaya = maaya

        self.palette = maaya.theme.Palette

        self.label = QLabel()

        self.label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.label.setStyleSheet(
            f"color: {self.palette.PRIMARY};"
        )

        self.setFocusPolicy(
            Qt.FocusPolicy.NoFocus
        )

        self.label.setFocusPolicy(
            Qt.FocusPolicy.NoFocus
        )

        self.label.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents,
            True
        )

        self.label.hide()

    def show_content(self, path):

        pixmap = QPixmap(str(path))

        if pixmap.isNull():

            self.label.setText(
                "Failed to load image."
            )

            self.label.show()

            return

        self.label.setPixmap(pixmap)

        self.label.show()

    def clear(self):

        self.label.clear()

        self.label.hide()