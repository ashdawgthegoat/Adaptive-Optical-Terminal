import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, 
    QLabel, QStackedWidget, QPlainTextEdit
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QPixmap

from screens.observe_screen import ObserveScreen
from screens.main_menu_screen import MainMenuScreen
from screens.initialization_screen import InitializationScreen
from screens.splash_screen import SplashScreen

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
        self.observe_screen = ObserveScreen(
            self.transition_to_main_menu
        )

        self.main_menu_screen.enter_callback = (
            self.handle_menu_selection
        )

        # Add Screens to Stack
        self.stacked_widget.addWidget(self.splash_screen)
        self.stacked_widget.addWidget(self.init_screen)
        self.stacked_widget.addWidget(self.main_menu_screen)
        self.stacked_widget.addWidget(self.observe_screen)

    def transition_to_initialization(self):
        """Switches to the initialization screen and starts the logs."""
        self.stacked_widget.setCurrentWidget(self.init_screen)
        self.init_screen.start_initialization()

    def transition_to_main_menu(self):
        """Switches to the main menu screen."""
        self.stacked_widget.setCurrentWidget(self.main_menu_screen)
        # Give focus to the main menu screen so it can receive key events immediately
        self.main_menu_screen.setFocus()
    
    def handle_menu_selection(self, selected_item):
        if selected_item == "OBSERVE":
            self.stacked_widget.setCurrentWidget(
                self.observe_screen
            )

            self.observe_screen.setFocus()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())