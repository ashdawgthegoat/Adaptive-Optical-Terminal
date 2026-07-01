from PyQt6.QtCore import (
    QObject,
    pyqtSignal
)

class Kaizen(QObject):

    focus_changed = pyqtSignal(str)

    def __init__(self):

        super().__init__()

        self.mode = "native"

        self.current_region = "navigation"

        self.panel_locked = False

        self.native_graph = {

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

        #Generated graph for workbench panels, will be populated by the workbench

        self.workbench_graph = {}

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

        graph = self.active_graph()

        if name not in graph:

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

        neighbours = self.active_graph().get(
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

    def set_mode(self, mode):

        if mode not in (
            "native",
            "workbench"
        ):
            return

        self.mode = mode


    def load_workbench_graph(self, graph):

        self.workbench_graph = graph


    def active_graph(self):

        if self.mode == "native":

            return self.native_graph

        return self.workbench_graph

    # ==========================================
    # Utilities
    # ==========================================

    def reset(self):

        self.current_index = 0

        self.initialize()