from PyQt6.QtWidgets import QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from widgets.renderers.base_renderer import BaseRenderer

class ImageRenderer(BaseRenderer):

    def __init__(self, maaya):

        super().__init__()

        self.maaya = maaya

        self.palette = maaya.theme.Palette

        self.label = QLabel()

        self.pixmap = None

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

        self.pixmap = QPixmap(str(path))

        if self.pixmap.isNull():

            self.label.setText(
                "Failed to load image."
            )

            self.label.show()

            return

        self.update_display()

        self.label.show()

    def resizeEvent(self, event):

        super().resizeEvent(event)

        self.update_display()

    def update_display(self):

        if self.pixmap is None:
            return

        scaled = self.pixmap.scaled(

            self.size(),

            Qt.AspectRatioMode.KeepAspectRatio,

            Qt.TransformationMode.SmoothTransformation

        )

        self.label.setPixmap(scaled)

    def update_display(self):

        if self.pixmap is None:
            return

        scaled = self.pixmap.scaled(
            self.label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        self.label.setPixmap(scaled)

    def refresh_presentation(self):

        self.palette = self.maaya.theme.Palette

        self.label.setStyleSheet(
            f"color: {self.palette.PRIMARY};"
        )

        self.update_display()

        self.update()

    def clear(self):

        self.label.clear()

        self.label.hide()