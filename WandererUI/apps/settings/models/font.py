from dataclasses import dataclass


# ==========================================================
# Font Model
#
# Represents a single font file on disk.
#
#   family — Font family name derived from the filename.
#   path   — Filesystem path to the font file.
#   active — Whether this font is currently applied.
# ==========================================================


@dataclass
class Font:

    family: str
    path: str
    active: bool = False
