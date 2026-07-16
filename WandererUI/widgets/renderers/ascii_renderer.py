from PyQt6.QtWidgets import QLabel, QVBoxLayout
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

        self.content = ""

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

        layout = QVBoxLayout(self)

        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.label)

        self.label.hide()

    def show_content(self, path):

        self.content = path.read_text(
            encoding="utf-8"
        )

        self.update_display()

        self.label.show()

    def show_file(self, path):

        self.show_content(path)

    def update_display(self):

        self.label.setText(
            self.content
        )

    def refresh_presentation(self):

        self.palette = self.maaya.theme.Palette

        self.typography = self.maaya.typography()

        self.label.setFont(
            QFont(
                self.maaya.font["family"],
                self.typography.BODY_SIZE
            )
        )

        self.label.setStyleSheet(
            f"color: {self.palette.PRIMARY};"
        )

        self.update_display()

        self.update()

    def clear(self):

        self.label.clear()

        self.label.hide()