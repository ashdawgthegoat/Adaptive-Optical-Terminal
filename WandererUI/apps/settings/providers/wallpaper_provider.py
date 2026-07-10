import os

from ..models.wallpaper import Wallpaper


# ==========================================================
# Wallpaper Provider
#
# Scans the wallpapers directory for available wallpaper
# assets. The directory is expected to contain two
# subdirectories:
#
#   static/  — Static images (.jpg, .jpeg, .png, .bmp, .txt)
#   live/    — Animated wallpapers (.mp4, .webm, .gif)
#
# ==========================================================


# ----------------------------------------------------------
# Supported Extensions
# ----------------------------------------------------------

STATIC_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".txt"}

LIVE_EXTENSIONS = {".mp4", ".webm", ".gif"}


class WallpaperProvider:

    # ======================================================
    # Initialisation
    # ======================================================

    def __init__(self, wallpapers_path: str):
        """
        Stores the filesystem path to the wallpapers root
        directory.
        """

        self._wallpapers_path = wallpapers_path

    # ======================================================
    # Wallpaper Discovery
    # ======================================================

    def list_wallpapers(self) -> list[Wallpaper]:
        """
        Scans both static/ and live/ subdirectories for
        wallpaper files with supported extensions.

        Returns a list of Wallpaper objects with the
        category set to the subdirectory name.
        """

        wallpapers = []

        categories = [
            ("static", STATIC_EXTENSIONS),
            ("live", LIVE_EXTENSIONS),
        ]

        for category, extensions in categories:

            category_dir = os.path.join(
                self._wallpapers_path,
                category
            )

            if not os.path.isdir(category_dir):

                continue

            for filename in sorted(os.listdir(category_dir)):

                ext = os.path.splitext(filename)[1].lower()

                if ext not in extensions:

                    continue

                file_path = os.path.join(
                    category_dir,
                    filename
                )

                if not os.path.isfile(file_path):

                    continue

                name = os.path.splitext(filename)[0]

                wallpapers.append(
                    Wallpaper(
                        name=name,
                        path=file_path,
                        category=category
                    )
                )

        return wallpapers
