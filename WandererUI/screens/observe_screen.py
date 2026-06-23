from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class ObserveScreen(QWidget):
    def __init__(self, return_callback):
        super().__init__()

        self.return_callback = return_callback

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("OBSERVE MODULE")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_font = QFont("Monospace", 32, QFont.Weight.Bold)
        title_font.setStyleHint(QFont.StyleHint.TypeWriter)

        title.setFont(title_font)
        title.setStyleSheet("color: white;")

        body = QLabel(
            "Future home of:\n\n"
            "Astronomy\n"
            "Astrophotography\n"
            "Wildlife Observation\n"
            "Spectroscopy\n"
            "Radio Astronomy"
        )

        body.setAlignment(Qt.AlignmentFlag.AlignCenter)

        body_font = QFont("Monospace", 16)
        body_font.setStyleHint(QFont.StyleHint.TypeWriter)

        body.setFont(body_font)
        body.setStyleSheet("color: white;")

        footer = QLabel("[ ESC ] Return")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("color: gray;")

        layout.addWidget(title)
        layout.addSpacing(40)
        layout.addWidget(body)
        layout.addSpacing(40)
        layout.addWidget(footer)

        self.setLayout(layout)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.return_callback()
        else:
            super().keyPressEvent(event)