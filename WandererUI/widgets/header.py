from PyQt6.QtWidgets import (
    QLabel,
    QHBoxLayout,
)

from PyQt6.QtCore import (
    Qt,
    pyqtSignal,
)

from PyQt6.QtGui import QFont

from widgets.layer.panel import Panel

from widgets.header_widgets.system_widget import SystemWidget
from widgets.header_widgets.environment_widget import EnvironmentWidget
from widgets.header_widgets.runtime_widget import RuntimeWidget
from widgets.header_widgets.clock_widget import ClockWidget

# ==========================================================
# Header
#
# Displays the global identity and controls of WandererUI.
# The Header is composed of multiple child panels responsible
# for system status, environment controls, runtime status
# and the system clock.
#
# This panel participates in the focus system and renders
# the standard panel border.
# ==========================================================

class Header(Panel):

    left_requested = pyqtSignal()

    right_requested = pyqtSignal()

    up_requested = pyqtSignal()

    down_requested = pyqtSignal()

    activated = pyqtSignal()

    def __init__(
        self,
        maaya,
        title="WANDERER",
        subtitle="MK II Alpha"
    ):

        super().__init__(maaya, show_border=True)

        self.maaya = maaya

        self.palette = self.maaya.theme.Palette

        self.spacing = self.maaya.theme.Spacing

        self.typography = self.maaya.typography()

        self.title = QLabel(title)

        self.subtitle = QLabel(subtitle)

        self.system_widget = SystemWidget(self.maaya)
        self.environment_widget = EnvironmentWidget(self.maaya)
        self.runtime_widget = RuntimeWidget(self.maaya)
        self.clock_widget = ClockWidget(self.maaya)

        self.build_ui()

    # ==========================================================
    # UI Construction
    # ==========================================================

    def build_ui(self):

        self.title.setFont(
            QFont(
                self.maaya.font["family"],
                self.typography.TITLE_SIZE
            )
        )

        self.subtitle.setFont(
            QFont(
                self.maaya.font["family"],
                self.typography.BODY_SIZE
            )
        )

        self.title.setStyleSheet(
            f"color: {self.palette.PRIMARY};"
        )

        self.subtitle.setStyleSheet(
            f"color: {self.palette.ACCENT};"
        )

        self.title.setAlignment(
            Qt.AlignmentFlag.AlignLeft
        )

        title_layout = QHBoxLayout()

        title_layout.setSpacing(
            self.spacing.ITEM_SPACING
        )

        title_layout.addWidget(
            self.title
        )

        title_layout.addWidget(
            self.subtitle
        )

        main_layout = QHBoxLayout()

        padding = self.content_padding()

        main_layout.setContentsMargins(
            padding,
            padding,
            padding,
            padding
        )

        # ==========================================================
        # Left Section
        # ==========================================================

        main_layout.addLayout(
            title_layout
        )

        # Push the runtime widget towards the centre.
        main_layout.addStretch()

        # ==========================================================
        # Centre Section
        # ==========================================================

        main_layout.addWidget(
            self.runtime_widget,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        main_layout.addSpacing(20)

        main_layout.addWidget(
            self.clock_widget,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        # Push the remaining widgets to the right.
        main_layout.addStretch()

        # ==========================================================
        # Right Section
        # ==========================================================

        main_layout.addWidget(
            self.environment_widget
        )

        main_layout.addSpacing(80)

        main_layout.addWidget(
            self.system_widget
        )

        self.setLayout(
            main_layout
        )

        self.set_inactive()
    
    # ==========================================================
    # Header State
    # ==========================================================

    def set_title(
        self,
        title,
        subtitle=None
    ):

        self.title.setText(
            title
        )

        self.subtitle.setAlignment(
            Qt.AlignmentFlag.AlignVCenter
        )

        if subtitle is not None:

            self.subtitle.setText(
                subtitle
            )

        self.subtitle.setStyleSheet(
            f"color: {self.palette.ACCENT};"
        )

    # ==========================================================
    # Keyboard Interaction
    # ==========================================================

    def keyPressEvent(
        self,
        event
    ):

        match event.key():

            case Qt.Key.Key_Left:
                self.left_requested.emit()

            case Qt.Key.Key_Right:
                self.right_requested.emit()

            case Qt.Key.Key_Up:
                self.up_requested.emit()

            case Qt.Key.Key_Down:
                self.down_requested.emit()

            case Qt.Key.Key_Return | Qt.Key.Key_Enter:
                self.activated.emit()

            case _:
                super().keyPressEvent(
                    event
                )
    
    # ==========================================================
    # Mouse Interaction
    # ==========================================================

    def mousePressEvent(
        self,
        event
    ):

        if event.button() == Qt.MouseButton.LeftButton:

            self.activated.emit()

        super().mousePressEvent(
            event
        )