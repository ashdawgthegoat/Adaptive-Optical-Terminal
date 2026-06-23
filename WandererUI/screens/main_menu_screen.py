from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class MainMenuScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.enter_callback = None  # Placeholder for enter key callback

        self.menu_items = [
            "OBSERVE",
            "ARCHIVE",
            "MUSIC",
            "MODULES",
            "SYSTEM"
        ]
        self.current_selection = 0
        self.item_labels = []
        
        # Enable keyboard focus for this widget
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
        self.init_ui()
        self.update_menu()

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
        
        menu_font = QFont("Monospace", 24)
        menu_font.setStyleHint(QFont.StyleHint.TypeWriter)

        for _ in self.menu_items:
            item_label = QLabel()
            item_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            item_label.setFont(menu_font)
            item_label.setStyleSheet("color: white;")
            self.item_labels.append(item_label)
            layout.addWidget(item_label)
            layout.addSpacing(20)

        self.setLayout(layout)

    def update_menu(self):
        """Updates the text of the menu labels to reflect the current selection."""
        # Find the max length to pad strings, keeping them perfectly aligned
        max_len = max(len(item) for item in self.menu_items)
        
        for i, label in enumerate(self.item_labels):
            # Pad the item to ensure uniform length for perfect center alignment
            padded_item = self.menu_items[i].ljust(max_len)
            
            if i == self.current_selection:
                label.setText(f"> {padded_item}")
            else:
                label.setText(f"  {padded_item}")

    def keyPressEvent(self, event):
        """Handles keyboard navigation."""
        if event.key() == Qt.Key.Key_Up:
            # Move up and wrap around
            self.current_selection = (self.current_selection - 1) % len(self.menu_items)
            self.update_menu()
        elif event.key() == Qt.Key.Key_Down:
            # Move down and wrap around
            self.current_selection = (self.current_selection + 1) % len(self.menu_items)
            self.update_menu()
        elif event.key() in (
            Qt.Key.Key_Return,
            Qt.Key.Key_Enter
        ):
            if self.enter_callback:
                self.enter_callback(
                    self.menu_items[
                        self.current_selection
                    ]
                )

        else:
            # Pass unhandled events to the base class
            super().keyPressEvent(event)