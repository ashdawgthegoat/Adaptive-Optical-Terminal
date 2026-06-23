import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QLabel, QStackedWidget, QPlainTextEdit
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPixmap

class SplashScreen(QWidget):
    def __init__(self, transition_callback):
        super().__init__()
        self.transition_callback = transition_callback
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo_label = QLabel()

        pixmap = QPixmap(
            "WandererUI/assets/WandererLogo.png"
        )

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


class InitializationScreen(QWidget):
    def __init__(self, transition_callback):
        super().__init__()
        self.transition_callback = transition_callback
        self.init_ui()
        
        # Define the logs to display
        self.logs = [
            "[ OK ] Storage Mounted",
            "[ OK ] Audio Service Started",
            "[ OK ] Observation Database Loaded",
            "[ OK ] Module Manager Started",
            "[ OK ] System Ready"
        ]
        self.current_log_index = 0
        
        # Timer for sequential log display
        self.log_timer = QTimer()
        self.log_timer.timeout.connect(self.display_next_log)

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50) # Padding for the terminal text

        self.terminal_output = QPlainTextEdit()
        self.terminal_output.setReadOnly(True)
        self.terminal_output.setFrameStyle(0) # Remove border
        self.terminal_output.setStyleSheet("background-color: black; color: white;")
        
        # Set monospace font
        terminal_font = QFont("Monospace")
        terminal_font.setStyleHint(QFont.StyleHint.TypeWriter)
        terminal_font.setPointSize(12)
        self.terminal_output.setFont(terminal_font)

        layout.addWidget(self.terminal_output)
        self.setLayout(layout)

    def start_initialization(self):
        """Starts the sequential log printing process."""
        self.current_log_index = 0
        self.terminal_output.clear()
        # Delay between each log entry (e.g., 600ms)
        self.log_timer.start(600)

    def display_next_log(self):
        """Appends the next log to the terminal output."""
        if self.current_log_index < len(self.logs):
            self.terminal_output.appendPlainText(self.logs[self.current_log_index])
            self.current_log_index += 1
        else:
            self.log_timer.stop()
            # Wait 1 second (1000 ms) before transitioning
            QTimer.singleShot(1000, self.transition_callback)


class MainMenuScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Title
        title_label = QLabel("WANDERER")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont("Monospace", 48, QFont.Weight.Bold)
        title_font.setStyleHint(QFont.StyleHint.TypeWriter)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: white; letter-spacing: 10px;")
        
        layout.addWidget(title_label)
        layout.addSpacing(60)

        # Menu Items
        menu_items = [
            "OBSERVE",
            "ARCHIVE",
            "MUSIC",
            "MODULES",
            "SYSTEM"
        ]
        
        menu_font = QFont("Monospace", 24)
        menu_font.setStyleHint(QFont.StyleHint.TypeWriter)

        for item in menu_items:
            item_label = QLabel(item)
            item_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            item_label.setFont(menu_font)
            item_label.setStyleSheet("color: white;")
            layout.addWidget(item_label)
            layout.addSpacing(20)

        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wanderer UI")
        
        # Application-wide styles
        self.setStyleSheet("background-color: black;")
        
        # Launch Fullscreen
        self.showFullScreen()

        # Main Central Widget to hold our screens
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Initialize Screens
        self.splash_screen = SplashScreen(self.transition_to_initialization)
        self.init_screen = InitializationScreen(self.transition_to_main_menu)
        self.main_menu_screen = MainMenuScreen()

        # Add Screens to Stack
        self.stacked_widget.addWidget(self.splash_screen)
        self.stacked_widget.addWidget(self.init_screen)
        self.stacked_widget.addWidget(self.main_menu_screen)

    def transition_to_initialization(self):
        """Switches to the initialization screen and starts the logs."""
        self.stacked_widget.setCurrentWidget(self.init_screen)
        self.init_screen.start_initialization()

    def transition_to_main_menu(self):
        """Switches to the main menu screen."""
        self.stacked_widget.setCurrentWidget(self.main_menu_screen)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())