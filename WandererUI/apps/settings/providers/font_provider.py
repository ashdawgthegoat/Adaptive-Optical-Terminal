import os

from ..models.font import Font


# ==========================================================
# Font Provider
#
# Recursively scans a fonts directory for available font
# files. Supported formats: .otf, .ttf, .woff, .woff2
#
# The font family name is derived from the filename by
# removing the extension and replacing hyphens and
# underscores with spaces.
# ==========================================================


FONT_EXTENSIONS = {".otf", ".ttf", ".woff", ".woff2"}


class FontProvider:

    # ======================================================
    # Initialisation
    # ======================================================

    def __init__(self, fonts_path: str):
        """
        Stores the filesystem path to the fonts root
        directory.
        """

        self._fonts_path = fonts_path

    # ======================================================
    # Font Discovery
    # ======================================================

    def list_fonts(self) -> list[Font]:
        """
        Recursively scans for font files with supported
        extensions.

        The family name is derived from the filename by
        removing the extension and replacing hyphens and
        underscores with spaces.

        Returns a list of Font objects.
        """

        fonts = []

        if not os.path.isdir(self._fonts_path):

            return fonts

        for root, _dirs, files in os.walk(self._fonts_path):

            for filename in sorted(files):

                ext = os.path.splitext(filename)[1].lower()

                if ext not in FONT_EXTENSIONS:

                    continue

                file_path = os.path.join(root, filename)

                # Derive the family name from the filename.

                base = os.path.splitext(filename)[0]

                family = base.replace("-", " ").replace(
                    "_", " "
                )

                fonts.append(
                    Font(
                        family=family,
                        path=file_path
                    )
                )

        return fonts
