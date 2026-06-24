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
from screens.astronomy_screen import AstronomyScreen
from screens.new_observation_screen import (NewObservationScreen)

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
        self.observe_screen = ObserveScreen(self.transition_to_main_menu)
        self.astronomy_screen = AstronomyScreen(self.transition_to_observe_menu)
        self.astronomy_screen.enter_callback = (self.handle_astronomy_selection)
        self.new_observation_screen = NewObservationScreen(self.transition_to_astronomy)
        self.observe_screen.enter_callback = (self.handle_observe_selection)

        self.main_menu_screen.enter_callback = (self.handle_menu_selection)

        # Add Screens to Stack
        self.stacked_widget.addWidget(self.splash_screen)
        self.stacked_widget.addWidget(self.init_screen)
        self.stacked_widget.addWidget(self.main_menu_screen)
        self.stacked_widget.addWidget(self.observe_screen)
        self.stacked_widget.addWidget(self.astronomy_screen)
        self.stacked_widget.addWidget(self.new_observation_screen)

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

    def transition_to_astronomy(self):
        self.stacked_widget.setCurrentWidget(
            self.astronomy_screen
        )

        self.astronomy_screen.setFocus()
    
    def transition_to_observe_menu(self):
        self.stacked_widget.setCurrentWidget(
            self.observe_screen
        )

        self.observe_screen.setFocus()
    
    def transition_to_new_observation(self):

        self.stacked_widget.setCurrentWidget(
            self.new_observation_screen
        )

        QTimer.singleShot(
            100,
            lambda: (
                self.new_observation_screen.name_input.setFocus(),
                self.new_observation_screen.name_input.activateWindow()
            )
        )

    def handle_astronomy_selection(self,selected_item):
        if selected_item == "New Observation":
            self.transition_to_new_observation()
    
    def transition_to_new_observation(self):

        self.stacked_widget.setCurrentWidget(
            self.new_observation_screen
        )

        self.new_observation_screen.setFocus()
    
    def handle_observe_selection(self,selected_item):
        if selected_item == "Astronomy":
            self.transition_to_astronomy()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())