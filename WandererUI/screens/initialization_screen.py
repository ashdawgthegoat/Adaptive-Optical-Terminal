from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

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