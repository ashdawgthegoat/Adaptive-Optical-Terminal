from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPixmap
from pathlib import Path

class SplashScreen(QWidget):
    def __init__(self, transition_callback):
        super().__init__()
        self.transition_callback = transition_callback
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo_label = QLabel()

        BASE_DIR = Path(__file__).resolve().parent.parent

        pixmap = QPixmap(
            str(BASE_DIR / "assets" / "WandererLogo.png")
        )

        if pixmap.isNull():
            print("Error: Wanderer Logo image not found.")

        logo_label.setPixmap(
            pixmap.scaled(
                220,
                220,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_font = QFont("Arial", 60, QFont.Weight.Bold)
        logo_label.setFont(logo_font)
        logo_label.setStyleSheet("color: white;")

        # Title
        title_label = QLabel("THE WANDERER PROJECT")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont("Arial", 32, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: white;")

        # Subtitle
        subtitle_label = QLabel("Scientific Observation Terminal\nMK II Alpha")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_font = QFont("Arial", 16)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setStyleSheet("color: #AAAAAA;") # Slightly dimmed white

        # Add widgets to layout with spacing
        layout.addWidget(logo_label)
        layout.addSpacing(40)
        layout.addWidget(title_label)
        layout.addSpacing(20)
        layout.addWidget(subtitle_label)

        self.setLayout(layout)

        # Trigger the transition callback after 3 seconds (3000 ms)
        QTimer.singleShot(3000, self.transition_callback)