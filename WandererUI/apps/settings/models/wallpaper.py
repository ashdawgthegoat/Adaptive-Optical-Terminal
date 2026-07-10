from dataclasses import dataclass


# ==========================================================
# Wallpaper Model
#
# Represents a single wallpaper asset on disk.
#
#   name     — Display name of the wallpaper.
#   path     — Filesystem path to the image or video file.
#   category — Either "static" or "live".
#   active   — Whether this wallpaper is currently applied.
# ==========================================================


@dataclass
class Wallpaper:

    name: str
    path: str
    category: str
    active: bool = False
