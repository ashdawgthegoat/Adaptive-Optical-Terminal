from PyQt6.QtGui import QFont

FONT_NAME = "System"
FONT_FAMILY = "Monospace"


class Typography:

    TITLE = QFont(
        FONT_FAMILY,
        28,
        QFont.Weight.Bold
    )

    SECTION = QFont(
        FONT_FAMILY,
        16,
        QFont.Weight.Bold
    )

    BODY = QFont(
        FONT_FAMILY,
        12
    )

    SMALL = QFont(
        FONT_FAMILY,
        10
    )

    SUBTITLE = QFont(
        FONT_FAMILY,
        12
    )

    HEADER = TITLE

    FOOTER = SMALL