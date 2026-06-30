from pathlib import Path
import importlib.util

from PyQt6.QtCore import (
    QObject,
    QTimer,
    pyqtSignal,
)


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
        self.typography = None
        self.wallpaper = None
        self.icon_pack = None

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

    def available_wallpapers(self,category="static"):

        return self.available_packages(
            f"wallpapers/{category}"
        )

    def available_icons(self):

        return self.available_packages("icons")

    # =====================================================
    # Generic Package Loader
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

    def load_font(self, package):

        self.typography = self.load_package(
            "fonts",
            package
        )

        return self.typography

    def load_wallpaper(self,category,package):

        folder = (
            self.assets_root
            / "wallpapers"
            / category
            / package
        )

        if not folder.exists():

            return None

        supported = {
            ".txt": "ascii",
            ".png": "image",
            ".jpg": "image",
            ".jpeg": "image",
            ".gif": "live",
            ".mp4": "live",
        }

        for file in folder.iterdir():

            suffix = file.suffix.lower()

            if suffix in supported:

                self.wallpaper = {

                    "type": supported[suffix],

                    "path": file,

                    "package": package,

                    "category": category

                }

                return self.wallpaper

        return None

    def load_icon_pack(self, package):

        self.icon_pack = self.load_package(
            "icons",
            package
        )

        return self.icon_pack

    # =====================================================
    # Animation
    # =====================================================

    def set_animation(self, name):

        self.stop()

        self.frames.clear()

        self.current_index = 0

        folder = (
            self.assets_root
            / "animations"
            / name
        )

        if not folder.exists():
            return

        files = sorted(folder.glob("*.txt"))

        for file in files:

            self.frames.append(
                file.read_text(
                    encoding="utf-8"
                )
            )

        if self.frames:

            self.frame_changed.emit(
                self.frames[0]
            )

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