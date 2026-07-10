# =============================================================================
# Settings Application — Theme Constants & Stylesheet
# =============================================================================
#
# Wanderer Classic visual language: retro-futuristic engineering terminal.
# No rounded corners, no glassmorphism, no shadows, no gradients.
# Sharp corners, monospace font, dark palette with red accent.
#
# =============================================================================

from PyQt6.QtGui import QFontDatabase


# =============================================================================
# Palette
# =============================================================================

class Palette:
    """Color constants for the Wanderer Classic theme."""

    BACKGROUND = "#050505"
    SURFACE = "#111111"
    PRIMARY = "#F2F2F2"
    SECONDARY = "#8A8A8A"
    ACCENT = "#A32626"
    SEPARATOR = "#303030"
    SURFACE_HOVER = "#1A1A1A"
    SURFACE_SELECTED = "#1F1A1A"


# =============================================================================
# Font Constants
# =============================================================================

FONT_FAMILY = "Departure Mono Nerd Font"
FONT_SIZE = 13


# =============================================================================
# Font Loader
# =============================================================================

def load_font(font_path: str) -> bool:
    """Load a font file into the application font database.

    Args:
        font_path: Absolute path to the font file (.otf or .ttf).

    Returns:
        True if the font was loaded successfully, False otherwise.
    """
    font_id = QFontDatabase.addApplicationFont(font_path)
    return font_id != -1


# =============================================================================
# Stylesheet Builder
# =============================================================================

def build_stylesheet() -> str:
    """Build the complete QSS stylesheet for the Wanderer Classic theme.

    Returns:
        A QSS stylesheet string that styles the entire application.
    """
    p = Palette

    return f"""
        /* ================================================================= */
        /* Global Defaults                                                   */
        /* ================================================================= */

        * {{
            font-family: "{FONT_FAMILY}";
            font-size: {FONT_SIZE}px;
            color: {p.PRIMARY};
            background-color: transparent;
            border: none;
            border-radius: 0px;
            outline: none;
        }}

        QMainWindow {{
            background-color: {p.BACKGROUND};
        }}

        QWidget {{
            background-color: transparent;
        }}

        /* ================================================================= */
        /* Labels                                                            */
        /* ================================================================= */

        QLabel {{
            color: {p.PRIMARY};
            background-color: transparent;
            padding: 0px;
        }}

        /* ================================================================= */
        /* Frames                                                            */
        /* ================================================================= */

        QFrame {{
            background-color: transparent;
            border: none;
        }}

        /* ================================================================= */
        /* Scroll Areas                                                      */
        /* ================================================================= */

        QScrollArea {{
            background-color: transparent;
            border: none;
        }}

        QScrollArea > QWidget > QWidget {{
            background-color: transparent;
        }}

        /* ================================================================= */
        /* Scrollbars                                                        */
        /* ================================================================= */

        QScrollBar:vertical {{
            background-color: {p.SURFACE};
            width: 8px;
            margin: 0px;
            border: none;
        }}

        QScrollBar::handle:vertical {{
            background-color: {p.SECONDARY};
            min-height: 30px;
            border: none;
        }}

        QScrollBar::handle:vertical:hover {{
            background-color: {p.PRIMARY};
        }}

        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {{
            height: 0px;
            border: none;
        }}

        QScrollBar::add-page:vertical,
        QScrollBar::sub-page:vertical {{
            background-color: {p.SURFACE};
        }}

        QScrollBar:horizontal {{
            background-color: {p.SURFACE};
            height: 8px;
            margin: 0px;
            border: none;
        }}

        QScrollBar::handle:horizontal {{
            background-color: {p.SECONDARY};
            min-width: 30px;
            border: none;
        }}

        QScrollBar::handle:horizontal:hover {{
            background-color: {p.PRIMARY};
        }}

        QScrollBar::add-line:horizontal,
        QScrollBar::sub-line:horizontal {{
            width: 0px;
            border: none;
        }}

        QScrollBar::add-page:horizontal,
        QScrollBar::sub-page:horizontal {{
            background-color: {p.SURFACE};
        }}

        /* ================================================================= */
        /* List Widgets                                                      */
        /* ================================================================= */

        QListWidget {{
            background-color: {p.SURFACE};
            border: none;
            outline: none;
        }}

        QListWidget::item {{
            color: {p.PRIMARY};
            background-color: transparent;
            padding: 6px 10px;
            border: none;
        }}

        QListWidget::item:hover {{
            background-color: {p.SURFACE_HOVER};
        }}

        QListWidget::item:selected {{
            background-color: {p.SURFACE_SELECTED};
            color: {p.PRIMARY};
            border-left: 3px solid {p.ACCENT};
        }}

        QListWidget::item:focus {{
            border: 1px solid {p.ACCENT};
        }}

        /* ================================================================= */
        /* Stacked Widget                                                    */
        /* ================================================================= */

        QStackedWidget {{
            background-color: transparent;
        }}

        /* ================================================================= */
        /* Push Buttons                                                      */
        /* ================================================================= */

        QPushButton {{
            background-color: {p.SURFACE};
            color: {p.PRIMARY};
            padding: 6px 16px;
            border: 1px solid {p.SEPARATOR};
        }}

        QPushButton:hover {{
            background-color: {p.SURFACE_HOVER};
        }}

        QPushButton:pressed {{
            background-color: {p.ACCENT};
        }}

        QPushButton:focus {{
            border: 1px solid {p.ACCENT};
        }}

        /* ================================================================= */
        /* Line Edits                                                        */
        /* ================================================================= */

        QLineEdit {{
            background-color: {p.SURFACE};
            color: {p.PRIMARY};
            padding: 4px 8px;
            border: 1px solid {p.SEPARATOR};
            selection-background-color: {p.ACCENT};
        }}

        QLineEdit:focus {{
            border: 1px solid {p.ACCENT};
        }}
    """
