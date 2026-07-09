from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from widgets.renderers.base_renderer import BaseRenderer


class AsciiRenderer(BaseRenderer):

    def __init__(self, maaya):

        super().__init__()

        self.maaya = maaya

        self.palette = maaya.theme.Palette
        self.typography = maaya.typography()

        self.label = QLabel()

        self.label.setFont(
            QFont(
                self.maaya.font["family"],
                self.typography.BODY_SIZE
            )
        )

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

        ascii_art = path.read_text(
            encoding="utf-8"
        )

        self.label.setText(
            ascii_art
        )

        self.label.show()

    def show_file(self, path):

        self.show_content(
            path.read_text(
                encoding="utf-8"
            )
        )

    def clear(self):

        self.label.clear()

        self.label.hide()