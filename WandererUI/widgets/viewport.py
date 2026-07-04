from PyQt6.QtWidgets import (
    QLabel,
    QWidget,
    QVBoxLayout,
    QScrollArea
)

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from PyQt6.QtGui import (
    QFont,
    QPixmap,
)

from widgets.panel import Panel

# ==========================================================
# Viewport
#
# Displays the primary content of the currently active
# application. Wallpapers, animations and future application
# views are rendered here.
#
# This panel participates in the focus system and renders
# the standard panel border.
# ==========================================================

class Viewport(Panel):

    next_requested = pyqtSignal()
    previous_requested = pyqtSignal()

    next_group_requested = pyqtSignal()
    previous_group_requested = pyqtSignal()

    def __init__(
        self,
        maaya
    ):

        super().__init__(
            maaya, 
            show_border=True
        )

        self.maaya = maaya

        self.wallpaper_types = [
            "static"
        ]

        self.wallpaper_type_index = 0

        self.wallpaper_index = {
            "static": 0,
        }

        self.palette = self.maaya.theme.Palette

        self.typography = self.maaya.typography()

        self.title = QLabel("VIEWPORT")

        self.ascii_display = QLabel()

        self.image_display = QLabel()

        self.maaya.frame_changed.connect(
            self.show_ascii
        )

        self.build_ui()

    # ==========================================================
    # UI Construction
    # ==========================================================

    def build_ui(self):

        layout = QVBoxLayout()

        padding = self.content_padding()

        layout.setContentsMargins(
            padding,    
            padding,
            padding,
            padding
        )

        self.scroll = QScrollArea()

        self.content = QWidget()

        self.content_layout = QVBoxLayout()

        self.content_layout.setContentsMargins(
            10,
            10,
            10,
            10
        )

        self.content_layout.setSpacing(0)

        self.title.setFont(
            QFont(
                self.maaya.font["family"],
                self.typography.SECTION_SIZE
            )
        )

        self.title.setStyleSheet(
            f"color: {self.palette.PRIMARY};"
        )

        self.title.setAlignment(
            Qt.AlignmentFlag.AlignLeft
        )

        self.content_layout.addWidget(
            self.title
        )

        self.content_layout.addStretch()

        # ==================================================
        # ASCII
        # ==================================================

        self.ascii_display.setFont(
            QFont(
                self.maaya.font["family"],
                self.typography.BODY_SIZE
            )
        )

        self.ascii_display.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.ascii_display.setStyleSheet(
            f"color: {self.palette.PRIMARY};"
        )

        # ==================================================
        # IMAGE
        # ==================================================

        self.image_display.setAlignment(
            Qt.AlignmentFlag.AlignCenter
    )

        self.image_display.setStyleSheet(
            f"color: {self.palette.PRIMARY};"
        )

        # ==================================================
        # Add renderers
        # ==================================================

        self.content_layout.addWidget(
            self.ascii_display,
            alignment=self.maaya.wallpaper_alignment
        )

        self.content_layout.addWidget(
            self.image_display,
            alignment=self.maaya.wallpaper_alignment
        )

        self.content_layout.addStretch()

        # ==========================================================
        # Hide all displays initially
        # =========================================================

        self.ascii_display.hide()

        self.image_display.hide()

        # ==========================================================

        self.content.setLayout(
            self.content_layout
        )

        self.scroll.setWidget(
            self.content
        )

        self.scroll.setWidgetResizable(
            True
        )

        self.scroll.setFrameShape(
            QScrollArea.Shape.NoFrame
        )

        self.scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        layout.addWidget(
            self.scroll
        )

        self.setLayout(
            layout
        )

        self.set_inactive()

    # ==========================================================
    # Public Interface
    #
    # These methods are used by native applications to control
    # what is rendered inside the Viewport.
    # ==========================================================

    # ==========================================================
    # Display Management
    # ==========================================================

    def show_ascii(
        self,
        ascii_art
    ):

        self.ascii_display.setText(
            ascii_art
        )

    def show_wallpaper(self):

        wallpaper = self.maaya.wallpaper

        if wallpaper is None:
            return

        self.hide_all_displays()

        match wallpaper["type"]:

            case "ascii":

                self.ascii_display.setText(
                    wallpaper["path"].read_text(
                        encoding="utf-8"
                    )
                )

                self.ascii_display.show()

            case "image":

                pixmap = QPixmap(
                    str(wallpaper["path"])
                )

                self.image_display.setPixmap(
                    pixmap
                )

                self.image_display.show()

    def next_wallpaper(self):

        self._change_wallpaper(1)

    def previous_wallpaper(self):

        self._change_wallpaper(-1)

    def next_type(self):

        self._change_type(1)

    def previous_type(self):

        self._change_type(-1)
    
    def _change_wallpaper(self, step):

        category = self.wallpaper_types[
            self.wallpaper_type_index
        ]

        wallpapers = self.maaya.available_wallpapers(category)

        if not wallpapers:
            return

        index = (
            self.wallpaper_index[category]
            + step
        ) % len(wallpapers)

        self.wallpaper_index[category] = index

        self.maaya.load_wallpaper(
            category,
            wallpapers[index]
        )

        self.show_wallpaper()


    def _change_type(self, step):

        self.wallpaper_type_index = (
            self.wallpaper_type_index
            + step
        ) % len(self.wallpaper_types)

        category = self.wallpaper_types[
            self.wallpaper_type_index
        ]

        wallpapers = self.maaya.available_wallpapers(category)

        if not wallpapers:
            self.clear()
            return

        index = self.wallpaper_index[category]

        self.maaya.load_wallpaper(
            category,
            wallpapers[index]
        )

        self.show_wallpaper()

    # ==========================================================
    # Animation Control
    # ==========================================================

    def play_animation(
        self,
        package,
        fps=10
    ):

        self.maaya.set_fps(
            fps
        )

        self.maaya.load_animation(
            "loading",
            package
        )

        self.maaya.play()

    def clear(self):

        self.hide_all_displays()

        self.ascii_display.clear()

        self.image_display.clear()

    # ==========================================================
    # Mouse Interaction
    # ==========================================================

    def mousePressEvent(
        self,
        event
    ):

        if event.button() == Qt.MouseButton.LeftButton:

            self.previous_requested.emit()

        elif event.button() == Qt.MouseButton.RightButton:

            self.next_requested.emit()

        super().mousePressEvent(
            event
        )

    def mouseDoubleClickEvent(
        self,
        event
    ):

        if event.button() == Qt.MouseButton.LeftButton:

            self.previous_group_requested.emit()

        elif event.button() == Qt.MouseButton.RightButton:

            self.next_group_requested.emit()

        super().mouseDoubleClickEvent(
            event
        )

    def move_left(self):

        self.previous_wallpaper()


    def move_right(self):

        self.next_wallpaper()


    def move_up(self):

        self.previous_type()


    def move_down(self):

        self.next_type()

    def hide_all_displays(self):

        self.ascii_display.hide()

        self.image_display.hide()