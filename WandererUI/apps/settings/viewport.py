from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QStackedLayout,
    QFrame,
)

from PyQt6.QtCore import Qt

from PyQt6.QtGui import QFont

from widgets.renderers.image_renderer import ImageRenderer
from widgets.renderers.ascii_renderer import AsciiRenderer


class SettingsViewport(QWidget):

    def __init__(
        self,
        maaya
    ):

        super().__init__()

        self.maaya = maaya

        self.stack = QStackedLayout()

        self.build_ui()

    # ======================================================
    # UI
    # ======================================================

    def build_ui(self):

        #
        # Appearance
        #

        self.appearance_page = QWidget()

        appearance_layout = QVBoxLayout()

        self.preview_container = QWidget()

        preview_layout = QVBoxLayout()

        preview_layout.setContentsMargins(
            0,
            20,
            0,
            20
        )

        preview_layout.setSpacing(0)

        self.preview_container.setLayout(
            preview_layout
        )

        self.appearance_title = QLabel(
            "Appearance Preview"
        )

        appearance_layout.addWidget(
            self.appearance_title
        )

        appearance_layout.addWidget(
            self.preview_container,
            stretch=1
        )

        self.appearance_title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.image_renderer = ImageRenderer(
            self.maaya
        )

        self.ascii_renderer = AsciiRenderer(
            self.maaya
        )

        self.font_preview = QLabel()

        self.theme_preview = QWidget()

        theme_layout = QVBoxLayout()

        theme_layout.setContentsMargins(
            40,
            20,
            40,
            20
        )

        theme_layout.setSpacing(8)

        self.theme_header = QFrame()

        self.theme_body = QFrame()

        self.theme_navigation = QFrame()

        self.theme_viewport = QFrame()

        self.theme_context = QFrame()

        self.theme_footer = QFrame()

        self.theme_header.setFixedHeight(24)

        self.theme_footer.setFixedHeight(18)

        self.theme_navigation.setFixedWidth(60)

        self.theme_context.setFixedWidth(60)

        body_layout = QHBoxLayout()

        body_layout.setSpacing(8)

        body_layout.addWidget(
            self.theme_navigation
        )

        body_layout.addWidget(
            self.theme_viewport,
            stretch=1
        )

        body_layout.addWidget(
            self.theme_context
        )

        theme_layout.addWidget(
            self.theme_header
        )

        theme_layout.addLayout(
            body_layout,
            stretch=1
        )

        theme_layout.addWidget(
            self.theme_footer
        )

        self.theme_preview.setLayout(
            theme_layout
        )

        preview_layout.addWidget(
            self.theme_preview
        )

        self.font_preview.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        appearance_layout.addWidget(
            self.appearance_title
        )

        preview_layout.addWidget(
            self.image_renderer
        )

        preview_layout.addWidget(
            self.ascii_renderer
        )

        preview_layout.addWidget(
            self.font_preview
        )

        self.appearance_page.setLayout(
            appearance_layout
        )

        #
        # Placeholder Pages
        #

        self.wifi_page = self.placeholder(
            "Wi-Fi"
        )

        self.bluetooth_page = self.placeholder(
            "Bluetooth"
        )

        self.audio_page = self.placeholder(
            "Audio"
        )

        self.modules_page = self.placeholder(
            "Modules"
        )

        self.about_page = self.placeholder(
            "About"
        )

        #
        # Stack
        #

        self.stack.addWidget(
            self.appearance_page
        )

        self.stack.addWidget(
            self.wifi_page
        )

        self.stack.addWidget(
            self.bluetooth_page
        )

        self.stack.addWidget(
            self.audio_page
        )

        self.stack.addWidget(
            self.modules_page
        )

        self.stack.addWidget(
            self.about_page
        )

        layout = QVBoxLayout()

        layout.addLayout(
            self.stack
        )

        self.setLayout(
            layout
        )

        self.show_page(
            "Appearance"
        )

    # ======================================================
    # Helpers
    # ======================================================

    def placeholder(
        self,
        title
    ):

        page = QLabel(
            f"{title}\n\nComing Soon"
        )

        page.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        return page

    # ======================================================
    # Pages
    # ======================================================

    def show_page(
        self,
        page
    ):

        mapping = {

            "Appearance":
                self.appearance_page,

            "Wi-Fi":
                self.wifi_page,

            "Bluetooth":
                self.bluetooth_page,

            "Audio":
                self.audio_page,

            "Modules":
                self.modules_page,

            "About":
                self.about_page,

        }

        self.stack.setCurrentWidget(
            mapping[page]
        )

    def show_renderer(
        self,
        renderer
    ):

        self.image_renderer.hide()

        self.ascii_renderer.hide()

        self.font_preview.hide()

        self.theme_preview.hide()

        renderer.show()

    # ======================================================
    # Appearance Preview
    # ======================================================

    def preview_theme(
        self,
        theme
    ):

        self.show_renderer(
            self.theme_preview
        )

        self.update_theme_preview()

    def preview_wallpaper(
        self,
        wallpaper
    ):

        self.stack.setCurrentWidget(
            self.appearance_page
        )

        self.font_preview.hide()

        self.image_renderer.hide()

        self.ascii_renderer.hide()

        match wallpaper["type"]:

            case "ascii":

                self.ascii_renderer.show()

                self.ascii_renderer.show_content(
                    wallpaper["path"]
                )

            case "image":

                self.image_renderer.show()

                self.image_renderer.show_content(
                    wallpaper["path"]
                )

            case "live":

                self.image_renderer.show()

                self.image_renderer.show_content(
                    wallpaper["path"]
                )

    def preview_font(
        self,
        family
    ):

        self.stack.setCurrentWidget(
            self.appearance_page
        )

        self.font_preview.show()

        self.font_preview.setFont(

            QFont(
                family,
                12
            )

        )

        self.font_preview.setText(

            "ABCDEFGHIJKLMNOPQRSTUVWXYZ\n"
            "abcdefghijklmnopqrstuvwxyz\n\n"
            "0123456789\n\n"
            "The quick brown fox jumps over the lazy dog.\n\n"
            "Veera Bhogya Vasundhara"

        )

    def update_theme_preview(self):

        palette = self.maaya.theme.Palette

        frames = [

            self.theme_header,

            self.theme_navigation,

            self.theme_viewport,

            self.theme_context,

            self.theme_footer,

        ]

        for frame in frames:

            frame.setStyleSheet(

                f"""

                background: {palette.BACKGROUND};

                border: 1px solid {palette.ACCENT};

                """

            )