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
from screens.new_observation_screen import (NewObservationScreen)
from screens.archive_screen import ArchiveScreen
from screens.observation_log_screen import ObservationLogScreen

# Module Imports
from screens.astronomy_screen import AstronomyScreen
from screens.astronomy_archive_screen import AstronomyArchiveScreen

from screens.astrophotography_screen import AstrophotographyScreen
from screens.astrophotography_archive_screen import AstrophotographyArchiveScreen

from screens.wildlife_screen import WildlifeScreen
from screens.wildlife_archive_screen import WildlifeArchiveScreen

from screens.spectroscopy_screen import SpectroscopyScreen
from screens.spectroscopy_archive_screen import SpectroscopyArchiveScreen

from screens.microscopy_screen import MicroscopyScreen
from screens.microscopy_archive_screen import MicroscopyArchiveScreen

from screens.radio_astronomy_screen import RadioAstronomyScreen
from screens.radio_astronomy_archive_screen import RadioAstronomyArchiveScreen


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

        # Track active modules to route back from shared screens properly
        self.active_module = "Astronomy"
        self.active_archive_module = "Astronomy"

        # Initialize Base Screens
        self.splash_screen = SplashScreen(self.transition_to_initialization)
        self.init_screen = InitializationScreen(self.transition_to_main_menu)
        self.main_menu_screen = MainMenuScreen()
        self.observe_screen = ObserveScreen(self.transition_to_main_menu)
        self.archive_screen = ArchiveScreen(self.transition_to_main_menu)
        
        self.new_observation_screen = NewObservationScreen(self.return_from_new_observation)
        self.observation_log_screen = ObservationLogScreen(self.return_from_observation_log)

        # Initialize Module Screens
        self.astronomy_screen = AstronomyScreen(self.transition_to_observe_menu)
        self.astronomy_archive_screen = AstronomyArchiveScreen(self.transition_to_archive, self.transition_to_observation_log)

        self.astrophotography_screen = AstrophotographyScreen(self.transition_to_observe_menu)
        self.astrophotography_archive_screen = AstrophotographyArchiveScreen(self.transition_to_archive, self.transition_to_observation_log)

        self.wildlife_screen = WildlifeScreen(self.transition_to_observe_menu)
        self.wildlife_archive_screen = WildlifeArchiveScreen(self.transition_to_archive, self.transition_to_observation_log)

        self.spectroscopy_screen = SpectroscopyScreen(self.transition_to_observe_menu)
        self.spectroscopy_archive_screen = SpectroscopyArchiveScreen(self.transition_to_archive, self.transition_to_observation_log)

        self.microscopy_screen = MicroscopyScreen(self.transition_to_observe_menu)
        self.microscopy_archive_screen = MicroscopyArchiveScreen(self.transition_to_archive, self.transition_to_observation_log)

        self.radio_astronomy_screen = RadioAstronomyScreen(self.transition_to_observe_menu)
        self.radio_astronomy_archive_screen = RadioAstronomyArchiveScreen(self.transition_to_archive, self.transition_to_observation_log)

        # Attach Callbacks
        self.main_menu_screen.enter_callback = (self.handle_menu_selection)
        self.observe_screen.enter_callback = (self.handle_observe_selection)
        self.archive_screen.enter_callback = (self.handle_archive_selection)

        self.astronomy_screen.enter_callback = (self.handle_astronomy_selection)
        self.astrophotography_screen.enter_callback = (self.handle_astrophotography_selection)
        self.wildlife_screen.enter_callback = (self.handle_wildlife_selection)
        self.spectroscopy_screen.enter_callback = (self.handle_spectroscopy_selection)
        self.microscopy_screen.enter_callback = (self.handle_microscopy_selection)
        self.radio_astronomy_screen.enter_callback = (self.handle_radio_astronomy_selection)

        # Add Screens to Stack
        self.stacked_widget.addWidget(self.splash_screen)
        self.stacked_widget.addWidget(self.init_screen)
        self.stacked_widget.addWidget(self.main_menu_screen)
        self.stacked_widget.addWidget(self.observe_screen)
        self.stacked_widget.addWidget(self.archive_screen)
        self.stacked_widget.addWidget(self.new_observation_screen)
        self.stacked_widget.addWidget(self.observation_log_screen)

        self.stacked_widget.addWidget(self.astronomy_screen)
        self.stacked_widget.addWidget(self.astronomy_archive_screen)
        
        self.stacked_widget.addWidget(self.astrophotography_screen)
        self.stacked_widget.addWidget(self.astrophotography_archive_screen)
        
        self.stacked_widget.addWidget(self.wildlife_screen)
        self.stacked_widget.addWidget(self.wildlife_archive_screen)
        
        self.stacked_widget.addWidget(self.spectroscopy_screen)
        self.stacked_widget.addWidget(self.spectroscopy_archive_screen)
        
        self.stacked_widget.addWidget(self.microscopy_screen)
        self.stacked_widget.addWidget(self.microscopy_archive_screen)
        
        self.stacked_widget.addWidget(self.radio_astronomy_screen)
        self.stacked_widget.addWidget(self.radio_astronomy_archive_screen)

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
        elif selected_item == "ARCHIVE":
            self.transition_to_archive()

    def transition_to_observe_menu(self):
        self.stacked_widget.setCurrentWidget(
            self.observe_screen
        )
        self.observe_screen.setFocus()

    def handle_observe_selection(self, selected_item):
        self.active_module = selected_item
        if selected_item == "Astronomy":
            self.transition_to_astronomy()
        elif selected_item == "Astrophotography":
            self.transition_to_astrophotography()
        elif selected_item == "Wildlife":
            self.transition_to_wildlife()
        elif selected_item == "Spectroscopy":
            self.transition_to_spectroscopy()
        elif selected_item == "Microscopy":
            self.transition_to_microscopy()
        elif selected_item == "Radio Astronomy":
            self.transition_to_radio_astronomy()

    def transition_to_archive(self):
        self.stacked_widget.setCurrentWidget(
            self.archive_screen
        )
        self.archive_screen.setFocus()

    def handle_archive_selection(self, selected_item):
        self.active_archive_module = selected_item
        if selected_item == "Astronomy":
            self.transition_to_astronomy_archive()
        elif selected_item == "Astrophotography":
            self.transition_to_astrophotography_archive()
        elif selected_item == "Wildlife":
            self.transition_to_wildlife_archive()
        elif selected_item == "Spectroscopy":
            self.transition_to_spectroscopy_archive()
        elif selected_item == "Microscopy":
            self.transition_to_microscopy_archive()
        elif selected_item == "Radio Astronomy":
            self.transition_to_radio_astronomy_archive()

    def transition_to_new_observation(self):
        
        self.new_observation_screen.set_category(
            self.active_module
        )

        self.stacked_widget.setCurrentWidget(
            self.new_observation_screen
        )

        self.new_observation_screen.name_input.clear()
        QTimer.singleShot(
            100,
            self.new_observation_screen.name_input.setFocus
        )

    def return_from_new_observation(self):
        if self.active_module == "Astronomy":
            self.transition_to_astronomy()
        elif self.active_module == "Astrophotography":
            self.transition_to_astrophotography()
        elif self.active_module == "Wildlife":
            self.transition_to_wildlife()
        elif self.active_module == "Spectroscopy":
            self.transition_to_spectroscopy()
        elif self.active_module == "Microscopy":
            self.transition_to_microscopy()
        elif self.active_module == "Radio Astronomy":
            self.transition_to_radio_astronomy()

    def transition_to_observation_log(self, observation_name):
        self.observation_log_screen.load_observation(
            observation_name
        )
        self.stacked_widget.setCurrentWidget(
            self.observation_log_screen
        )
        self.observation_log_screen.setFocus()

    def return_from_observation_log(self):
        if self.active_archive_module == "Astronomy":
            self.transition_to_astronomy_archive()
        elif self.active_archive_module == "Astrophotography":
            self.transition_to_astrophotography_archive()
        elif self.active_archive_module == "Wildlife":
            self.transition_to_wildlife_archive()
        elif self.active_archive_module == "Spectroscopy":
            self.transition_to_spectroscopy_archive()
        elif self.active_archive_module == "Microscopy":
            self.transition_to_microscopy_archive()
        elif self.active_archive_module == "Radio Astronomy":
            self.transition_to_radio_astronomy_archive()

    # ==========================
    # Astronomy Handlers
    # ==========================
    def transition_to_astronomy(self):
        self.stacked_widget.setCurrentWidget(self.astronomy_screen)
        self.astronomy_screen.setFocus()

    def transition_to_astronomy_archive(self):
        self.astronomy_archive_screen.load_observations()
        self.stacked_widget.setCurrentWidget(self.astronomy_archive_screen)
        self.astronomy_archive_screen.setFocus()
        
    def handle_astronomy_selection(self, selected_item):
        if selected_item == "New Observation":
            self.transition_to_new_observation()

    # ==========================
    # Astrophotography Handlers
    # ==========================
    def transition_to_astrophotography(self):
        self.stacked_widget.setCurrentWidget(self.astrophotography_screen)
        self.astrophotography_screen.setFocus()

    def transition_to_astrophotography_archive(self):
        self.astrophotography_archive_screen.load_observations()
        self.stacked_widget.setCurrentWidget(self.astrophotography_archive_screen)
        self.astrophotography_archive_screen.setFocus()
        
    def handle_astrophotography_selection(self, selected_item):
        if selected_item == "New Observation":
            self.transition_to_new_observation()

    # ==========================
    # Wildlife Handlers
    # ==========================
    def transition_to_wildlife(self):
        self.stacked_widget.setCurrentWidget(self.wildlife_screen)
        self.wildlife_screen.setFocus()

    def transition_to_wildlife_archive(self):
        self.wildlife_archive_screen.load_observations()
        self.stacked_widget.setCurrentWidget(self.wildlife_archive_screen)
        self.wildlife_archive_screen.setFocus()
        
    def handle_wildlife_selection(self, selected_item):
        if selected_item == "New Observation":
            self.transition_to_new_observation()

    # ==========================
    # Spectroscopy Handlers
    # ==========================
    def transition_to_spectroscopy(self):
        self.stacked_widget.setCurrentWidget(self.spectroscopy_screen)
        self.spectroscopy_screen.setFocus()

    def transition_to_spectroscopy_archive(self):
        self.spectroscopy_archive_screen.load_observations()
        self.stacked_widget.setCurrentWidget(self.spectroscopy_archive_screen)
        self.spectroscopy_archive_screen.setFocus()
        
    def handle_spectroscopy_selection(self, selected_item):
        if selected_item == "New Observation":
            self.transition_to_new_observation()

    # ==========================
    # Microscopy Handlers
    # ==========================
    def transition_to_microscopy(self):
        self.stacked_widget.setCurrentWidget(self.microscopy_screen)
        self.microscopy_screen.setFocus()

    def transition_to_microscopy_archive(self):
        self.microscopy_archive_screen.load_observations()
        self.stacked_widget.setCurrentWidget(self.microscopy_archive_screen)
        self.microscopy_archive_screen.setFocus()
        
    def handle_microscopy_selection(self, selected_item):
        if selected_item == "New Observation":
            self.transition_to_new_observation()

    # ==========================
    # Radio Astronomy Handlers
    # ==========================
    def transition_to_radio_astronomy(self):
        self.stacked_widget.setCurrentWidget(self.radio_astronomy_screen)
        self.radio_astronomy_screen.setFocus()

    def transition_to_radio_astronomy_archive(self):
        self.radio_astronomy_archive_screen.load_observations()
        self.stacked_widget.setCurrentWidget(self.radio_astronomy_archive_screen)
        self.radio_astronomy_archive_screen.setFocus()
        
    def handle_radio_astronomy_selection(self, selected_item):
        if selected_item == "New Observation":
            self.transition_to_new_observation()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())