from dataclasses import dataclass


# ==========================================================
# Theme Model
#
# Represents a single theme package on disk.
#
#   name   — Display name of the theme.
#   path   — Filesystem path to the theme directory.
#   active — Whether this theme is currently applied.
# ==========================================================


@dataclass
class Theme:

    name: str
    path: str
    active: bool = False
