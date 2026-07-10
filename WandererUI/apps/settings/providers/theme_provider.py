import json
import os

from ..models.theme import Theme


# ==========================================================
# Theme Provider
#
# Scans a themes directory on disk for available theme
# packages. Each theme is a subdirectory containing a
# metadata.json file with at least a "name" field.
#
# metadata.json format:
#
#   {
#       "id": "classic",
#       "name": "Wanderer Classic",
#       "author": "MADLAB",
#       "version": "1.0.0",
#       "description": "..."
#   }
#
# ==========================================================


class ThemeProvider:

    # ======================================================
    # Initialisation
    # ======================================================

    def __init__(self, themes_path: str):
        """
        Stores the filesystem path to the themes directory.
        """

        self._themes_path = themes_path

    # ======================================================
    # Theme Discovery
    # ======================================================

    def list_themes(self) -> list[Theme]:
        """
        Scans the themes directory for valid theme packages.

        Each subdirectory that contains a metadata.json file
        is treated as a theme. The display name is read from
        the "name" field in the metadata.

        Returns a list of Theme objects.
        """

        themes = []

        if not os.path.isdir(self._themes_path):

            return themes

        for entry in sorted(os.listdir(self._themes_path)):

            theme_dir = os.path.join(
                self._themes_path,
                entry
            )

            if not os.path.isdir(theme_dir):

                continue

            metadata_path = os.path.join(
                theme_dir,
                "metadata.json"
            )

            if not os.path.isfile(metadata_path):

                continue

            try:

                with open(metadata_path, "r") as f:

                    metadata = json.load(f)

                name = metadata.get("name", entry)

                themes.append(
                    Theme(
                        name=name,
                        path=theme_dir
                    )
                )

            except (json.JSONDecodeError, OSError):

                # Skip themes with invalid or unreadable
                # metadata files.

                continue

        return themes
