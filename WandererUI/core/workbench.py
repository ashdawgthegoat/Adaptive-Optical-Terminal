"""
workbench.py

Runtime environment for external Linux applications.

Workbench is responsible for hosting applications that are
not Wanderer-native.

The Header and Footer remain part of the Desktop while the
central workspace (Navigation, Viewport and Context) is
temporarily replaced by the Workbench.

This class intentionally contains no launching logic yet.
That will be implemented after the Desktop architecture
retrofit is complete.
"""

from PyQt6.QtWidgets import QWidget


class Workbench(QWidget):
    """
    Runtime environment for external Linux applications.
    """

    def __init__(self):

        super().__init__()

        self.active_application = None

    # ======================================================
    # Runtime
    # ======================================================

    def launch(self, application):
        """
        Launch an external application inside the Workbench.

        TODO:
        Embed or manage external application execution.
        """
        self.active_application = application

    def close(self):
        """
        Close the active external application.
        """
        self.active_application = None

    # ======================================================
    # State
    # ======================================================

    def is_running(self):

        return self.active_application is not None