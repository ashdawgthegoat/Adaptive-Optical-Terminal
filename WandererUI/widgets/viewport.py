from PyQt6.QtWidgets import (
    QLabel,
    QWidget,
    QVBoxLayout,
    QScrollArea
)

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from widgets.panel import Panel


class Viewport(Panel):

    next_requested = pyqtSignal()
    previous_requested = pyqtSignal()

    next_group_requested = pyqtSignal()
    previous_group_requested = pyqtSignal()

    def __init__(
        self,
        maaya
    ):

        super().__init__(maaya)

        self.maaya = maaya

        self.palette = self.maaya.theme.Palette

        self.typography = self.maaya.typography()

        self.title = QLabel("VIEWPORT")

        self.display = QLabel()

        self.maaya.frame_changed.connect(
            self.show_ascii
        )

        self.build_ui()

    def build_ui(self):

        layout = QVBoxLayout()

        self.scroll = QScrollArea()

        self.content = QWidget()

        self.content_layout = QVBoxLayout()

        self.content_layout.setContentsMargins(
            10,
            10,
            10,
            10
        )

        self.content_layout.setSpacing(0)

        self.title.setFont(
            QFont(
                self.maaya.font["family"],
                self.typography.SECTION_SIZE
            )
        )

        self.title.setStyleSheet(
            f"color: {self.palette.PRIMARY};"
        )

        self.title.setAlignment(
            Qt.AlignmentFlag.AlignLeft
        )

        self.content_layout.addWidget(
            self.title
        )

        self.content_layout.addStretch()

        self.display.setFont(
            QFont(
                self.maaya.font["family"],
                self.typography.BODY_SIZE
            )
        )

        self.display.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.display.setStyleSheet(
            f"color: {self.palette.PRIMARY};"
        )

        self.content_layout.addWidget(
            self.display,
            alignment=self.maaya.wallpaper_alignment
        )

        self.content_layout.addStretch()

        self.content.setLayout(
            self.content_layout
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

        layout.addWidget(
            self.scroll
        )

        self.setLayout(
            layout
        )

        self.set_inactive()

    def show_ascii(
        self,
        ascii_art
    ):

        self.display.setText(
            ascii_art
        )

    def show_wallpaper(self):

        wallpaper = self.maaya.wallpaper

        if wallpaper is None:
            return

        if wallpaper["type"] == "ascii":

            self.show_ascii(
                wallpaper["path"].read_text(
                    encoding="utf-8"
                )
            )

    def play_animation(
        self,
        package,
        fps=10
    ):

        self.maaya.set_fps(
            fps
        )

        self.maaya.load_animation(
            "loading",
            package
        )

        self.maaya.play()

    def clear(self):

        self.display.clear()

    def mousePressEvent(
        self,
        event
    ):

        if event.button() == Qt.MouseButton.LeftButton:

            self.previous_requested.emit()

        elif event.button() == Qt.MouseButton.RightButton:

            self.next_requested.emit()

        super().mousePressEvent(
            event
        )

    def mouseDoubleClickEvent(
        self,
        event
    ):

        if event.button() == Qt.MouseButton.LeftButton:

            self.previous_group_requested.emit()

        elif event.button() == Qt.MouseButton.RightButton:

            self.next_group_requested.emit()

        super().mouseDoubleClickEvent(
            event
        )