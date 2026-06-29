from PyQt6.QtWidgets import (
    QLabel,
    QWidget,
    QVBoxLayout,
    QScrollArea
)

from PyQt6.QtCore import Qt, pyqtSignal
from widgets.theme import (
    PRIMARY,
    BODY_FONT,
    SECTION_FONT
)

from services.maaya import Maaya
from widgets.panel import Panel

class Viewport(Panel):

    next_requested = pyqtSignal()
    previous_requested = pyqtSignal()

    next_group_requested = pyqtSignal()
    previous_group_requested = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.title = QLabel("VIEWPORT")

        self.display = QLabel()

        self.maaya = Maaya()

        self.maaya.frame_changed.connect(
            self.show_ascii
        )

        self.build_ui()

    def build_ui(self):

        layout = QVBoxLayout()

        self.scroll = QScrollArea()

        self.content = QWidget()

        self.content_layout = QVBoxLayout()

        self.content_layout.setContentsMargins(10, 10, 10, 10)

        self.content_layout.setSpacing(0)

        self.title.setFont(SECTION_FONT)
        self.title.setStyleSheet(f"color: {PRIMARY};")
        self.title.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.content_layout.addWidget(self.title)

        self.content_layout.addStretch()

        self.display.setFont(BODY_FONT)

        self.display.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.display.setStyleSheet(
            f"color: {PRIMARY};"
        )

        self.show_ascii(self.maaya.get_logo("wanderer"))

        self.content_layout.addWidget(
            self.display,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.content_layout.addStretch()

        self.content.setLayout(
            self.content_layout
        )

        self.scroll.setWidget(
            self.content
        )

        self.scroll.setWidgetResizable(True)

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

        self.setLayout(layout)

        self.set_inactive()

    def show_ascii(self,ascii_art):

        self.display.setText(
            ascii_art
        )
    
    def play_animation(self, name, fps=10):

        self.maaya.set_fps(fps)

        self.maaya.set_animation(name)

        self.maaya.play()

    def clear(self):

        self.display.clear()

    def mousePressEvent(self, event):

        if event.button() == Qt.MouseButton.LeftButton:

            self.previous_requested.emit()

        elif event.button() == Qt.MouseButton.RightButton:

            self.next_requested.emit()

        super().mousePressEvent(event)


    def mouseDoubleClickEvent(self, event):

        if event.button() == Qt.MouseButton.LeftButton:

            self.previous_group_requested.emit()

        elif event.button() == Qt.MouseButton.RightButton:

            self.next_group_requested.emit()

        super().mouseDoubleClickEvent(event)