from PyQt6.QtCore import (
    QObject,
    pyqtSignal
)

class Kaizen(QObject):

    focus_changed = pyqtSignal(str)

    def __init__(self):

        super().__init__()

        self.current_region = "navigation"

        self.panel_locked = False

        self.graph = {

            "navigation": {

                "up": "header",
                "right": "viewport",
                "down": "footer",
                "left": "context"

            },

            "header": {

                "down": "navigation"

            },

            "viewport": {

                "left": "navigation",
                "right": "context",
                "up": "header",
                "down": "footer"

            },

            "context": {

                "left": "viewport",
                "right": "navigation",
                "up": "header",
                "down": "footer"

            },

            "footer": {

                "up": "navigation"

            }

        }

    # ==========================================
    # Startup
    # ==========================================

    def initialize(self):

        self.current_region = "navigation"

        self.focus_changed.emit(
            self.current_region
        )

    # ==========================================
    # Focus
    # ==========================================

    def current(self):

        return self.current_region

    def set_focus(self, name):

        if name not in self.graph:

            return

        self.current_region = name

        self.focus_changed.emit(
            self.current_region
        )

    def has_focus(self, name):

        return self.current() == name

    def is_locked(self):

        return self.panel_locked


    def toggle_lock(self):

        self.panel_locked = not self.panel_locked

        return self.panel_locked


    def unlock(self):

        self.panel_locked = False

    # ==========================================
    # Navigation
    # ==========================================

    def move_left(self):

        self._move("left")


    def move_right(self):

        self._move("right")


    def move_up(self):

        self._move("up")


    def move_down(self):

        self._move("down")

    def _move(self, direction):

        if self.panel_locked:

            return

        neighbours = self.graph.get(
            self.current_region,
            {}
        )

        if direction in neighbours:

            self.current_region = neighbours[
                direction
            ]

            self.focus_changed.emit(
                self.current_region
            )

    # ==========================================
    # Utilities
    # ==========================================

    def reset(self):

        self.current_index = 0

        self.initialize()