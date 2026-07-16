from PyQt6.QtWidgets import (
    QLabel,
    QWidget,
    QVBoxLayout,
    QScrollArea
)

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from widgets.renderers.ascii_renderer import AsciiRenderer
from widgets.renderers.image_renderer import ImageRenderer

from widgets.layer.panel import Panel

# ==========================================================
# Viewport
#
#Displays the primary preview of WandererUI.
#The Viewport hosts wallpapers, animations and
#Core Applications.
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

        self.ascii_renderer = AsciiRenderer(
            self.maaya
        )

        self.image_renderer = ImageRenderer(
            self.maaya
        )

        self.preview = None

        #self.maaya.frame_changed.connect(
        #    self.ascii_renderer.show_content
        #)

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

        self.scroll.viewport().setFocusPolicy(
            Qt.FocusPolicy.NoFocus
        )

        self.content = QWidget()

        self.scroll.setFocusPolicy(
            Qt.FocusPolicy.NoFocus
        )

        self.content.setFocusPolicy(
            Qt.FocusPolicy.NoFocus
        )

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

        self.content_layout.addWidget(
            self.ascii_renderer,
            alignment=self.maaya.wallpaper_alignment
        )

        self.content_layout.addWidget(
            self.image_renderer,
            alignment=self.maaya.wallpaper_alignment
        )

        self.content_layout.addStretch()

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

    def show_wallpaper(self):

        if self.preview_active():
            return

        wallpaper = self.maaya.wallpaper

        if wallpaper is None:
            return

        self.hide_all_displays()

        match wallpaper["type"]:

            case "ascii":

                self.ascii_renderer.show_content(
                    wallpaper["path"]
                )

            case "image":

                self.image_renderer.show_content(
                    wallpaper["path"]
                )

    def current_category(self):

        return self.wallpaper_types[
            self.wallpaper_type_index
        ]


    def current_wallpapers(self):

        return self.maaya.available_wallpapers(
            self.current_category()
        )
    
    def _change_wallpaper(self, step):

        category = self.current_category()

        wallpapers = self.current_wallpapers()

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

        wallpapers = self.current_wallpapers()

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

        self.ascii_renderer.clear()

        self.image_renderer.clear()

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

        self._change_wallpaper(
            -1
        )


    def move_right(self):

        self._change_wallpaper(
            1
        )


    def move_up(self):

        self._change_type(
            -1
        )


    def move_down(self):

        self._change_type(
            1
        )

    def hide_all_displays(self):

        self.ascii_renderer.clear()

        self.image_renderer.clear()

    def show_preview(self, widget):
        """Display custom preview content inside the viewport."""

        self.hide_all_displays()

        if self.preview is not None:
            self.preview.setParent(None)

        self.preview = widget

        self.content_layout.insertWidget(
            2,
            widget,
            alignment=Qt.AlignmentFlag.AlignCenter
        )


    def hide_preview(self):
        """Remove the hosted preview."""

        if self.preview is None:
            return

        self.preview.setParent(None)

        self.preview = None

    def set_title(
        self,
        title
    ):

        self.title.setText(
            title.upper()
        )

    def refresh_presentation(self):

        self.palette = self.maaya.theme.Palette

        self.typography = self.maaya.typography()

        self.title.setFont(
            QFont(
                self.maaya.font["family"],
                self.typography.SECTION_SIZE
            )
        )

        self.title.setStyleSheet(
            f"color: {self.palette.PRIMARY};"
        )

        self.ascii_renderer.refresh_presentation()

        self.image_renderer.refresh_presentation()

        self.update()


    def preview_active(self):
        return self.preview is not None