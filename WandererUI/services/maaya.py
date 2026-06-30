from pathlib import Path
import importlib.util

from PyQt6.QtCore import (
    QObject,
    QTimer,
    pyqtSignal,
    Qt
)

from PyQt6.QtGui import QFontDatabase


class Maaya(QObject):

    frame_changed = pyqtSignal(str)

    def __init__(self):

        super().__init__()

        self.assets_root = Path("assets")

        self.cache = {}

        # =====================================
        # Active Presentation Packages
        # =====================================

        self.theme = None
        self.font = None
        self.wallpaper = None
        self.sound = None
        self.animation = None
        self.wallpaper_alignment = (
            Qt.AlignmentFlag.AlignCenter
        )

        # =====================================
        # Animation
        # =====================================

        self.frames = []
        self.current_index = 0
        self.fps = 10

        self.timer = QTimer()
        self.timer.timeout.connect(self.next_frame)

    # =====================================================
    # Generic Package Discovery
    # =====================================================

    def available_packages(self, category):

        directory = self.assets_root / category

        if not directory.exists():
            return []

        return sorted(
            folder.name
            for folder in directory.iterdir()
            if folder.is_dir()
        )

    def available_themes(self):

        return self.available_packages("themes")

    def available_fonts(self):

        return self.available_packages("fonts")

    def available_wallpapers(self, category="static"):

        directory = (
            self.assets_root
            / "wallpapers"
            / category
        )

        if not directory.exists():
            return []

        supported = {
            ".txt",
            ".png",
            ".jpg",
            ".jpeg",
            ".gif",
            ".mp4",
        }

        return sorted(

            file.name

            for file in directory.iterdir()

            if (
                file.is_file()
                and file.suffix.lower() in supported
            )

        )

    def available_sounds(self):

        directory = self.assets_root / "sounds"

        if not directory.exists():
            return []

        supported = {
            ".wav",
            ".mp3",
            ".ogg",
            ".flac",
        }

        return sorted(

            file.name

            for file in directory.iterdir()

            if (
                file.is_file()
                and file.suffix.lower() in supported
            )

        )

    def available_animations(
        self,
        category
    ):

        return self.available_packages(
            f"animations/{category}"
        )

    # =====================================================
    # Theme Loader
    # =====================================================

    def load_package(self, category, package):

        key = (category, package)

        if key in self.cache:
            return self.cache[key]

        definition = (
            self.assets_root
            / category
            / package
            / "definition.py"
        )

        if not definition.exists():
            return None

        spec = importlib.util.spec_from_file_location(
            f"{category}.{package}",
            definition
        )

        module = importlib.util.module_from_spec(spec)

        spec.loader.exec_module(module)

        self.cache[key] = module

        return module

    # =====================================================
    # Presentation
    # =====================================================

    def load_theme(self, package):

        self.theme = self.load_package(
            "themes",
            package
        )

        return self.theme

    def load_font(
        self,
        package
    ):

        folder = (
            self.assets_root
            / "fonts"
            / package
        )

        if not folder.exists():
            return None

        font_file = next(
            (
                file
                for file in folder.iterdir()
                if (
                    file.is_file()
                    and file.suffix.lower() in {
                        ".ttf",
                        ".otf"
                    }
                )
            ),
            None
        )

        if font_file is None:
            return None

        font_id = QFontDatabase.addApplicationFont(
            str(font_file)
        )

        if font_id == -1:
            return None

        family = QFontDatabase.applicationFontFamilies(
            font_id
        )

        if not family:
            return None

        typography = (
            folder
            / "typography.py"
        )

        if typography.exists():

            spec = importlib.util.spec_from_file_location(
                f"fonts.{package}.typography",
                typography
            )

            module = importlib.util.module_from_spec(spec)

            spec.loader.exec_module(module)

        else:

            module = None

        self.font = {

            "family": family[0],

            "typography": module,

            "package": package,

        }

        return self.font

    def typography(self):

        if (
            self.font
            and self.font["typography"]
        ):

            return self.font["typography"].Typography

        class DefaultTypography:

            TITLE_SIZE = 20

            SECTION_SIZE = 14

            BODY_SIZE = 12

            FOOTER_SIZE = 11

            MONO_SIZE = 12

        return DefaultTypography

    def load_wallpaper(
        self,
        category,
        filename
    ):

        file = (
            self.assets_root
            / "wallpapers"
            / category
            / filename
        )

        if not file.exists():

            return None

        supported = {

            ".txt": "ascii",

            ".png": "image",

            ".jpg": "image",

            ".jpeg": "image",

            ".gif": "live",

            ".mp4": "live",

        }

        wallpaper_type = supported.get(
            file.suffix.lower()
        )

        if wallpaper_type is None:

            return None

        self.wallpaper = {

            "type": wallpaper_type,

            "path": file,

            "filename": filename,

            "category": category,

        }

        return self.wallpaper

    def set_wallpaper_alignment(
        self,
        alignment
    ):

        self.wallpaper_alignment = alignment

    def load_sound(
        self,
        filename
    ):

        file = (
            self.assets_root
            / "sounds"
            / filename
        )

        if not file.exists():

            return None

        self.sound = file

        return self.sound

    # =====================================================
    # Animation
    # =====================================================

    def load_animation(
        self,
        category,
        package
    ):

        self.stop()

        self.frames.clear()

        self.current_index = 0

        folder = (
            self.assets_root
            / "animations"
            / category
            / package
        )

        if not folder.exists():
            return None

        files = sorted(
            file
            for file in folder.iterdir()
            if file.is_file()
        )

        if not files:
            return None

        frame_sequence = {
            ".txt",
            ".png",
            ".jpg",
            ".jpeg",
            ".svg",
        }

        native = {
            ".gif",
            ".mp4",
        }

        extension = files[0].suffix.lower()

        # -------------------------------------
        # Frame Sequence Animation
        # -------------------------------------

        if extension in frame_sequence:

            for file in files:

                if file.suffix.lower() != extension:
                    return None

            self.animation = {

                "type": "frames",

                "category": category,

                "package": package,

            }

            if extension == ".txt":

                for file in files:

                    self.frames.append(
                        file.read_text(
                            encoding="utf-8"
                        )
                    )

            else:

                self.frames.extend(files)

            if self.frames:

                self.frame_changed.emit(
                    self.frames[0]
                    if extension == ".txt"
                    else str(self.frames[0])
                )

            return self.animation

        # -------------------------------------
        # Native Animation
        # -------------------------------------

        if extension in native:

            if len(files) != 1:
                return None

            self.animation = {

                "type": "native",

                "path": files[0],

                "category": category,

                "package": package,

            }

            return self.animation

        return None

    def play(self):

        if not self.frames:
            return

        self.timer.start(
            int(1000 / self.fps)
        )

    def pause(self):

        self.timer.stop()

    def stop(self):

        self.timer.stop()

        self.current_index = 0

        if self.frames:

            self.frame_changed.emit(
                self.frames[0]
            )

    def next_frame(self):

        if not self.frames:
            return

        self.current_index += 1

        if self.current_index >= len(self.frames):
            self.current_index = 0

        self.frame_changed.emit(
            self.frames[
                self.current_index
            ]
        )

    def set_fps(self, fps):

        self.fps = fps

        if self.timer.isActive():
            self.play()

    def current_frame(self):

        if not self.frames:
            return ""

        return self.frames[
            self.current_index
        ]

    # =====================================================
    # Cache
    # =====================================================

    def clear_cache(self):

        self.cache.clear()