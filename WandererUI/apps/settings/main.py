#!/usr/bin/env python3
"""
Standalone Settings Application.

Launch with:
    python -m apps.settings.main

Or directly:
    python apps/settings/main.py
"""

from __future__ import annotations

import sys
import os

# Ensure the WandererUI root is on sys.path so relative imports work
# when running this file directly.
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.abspath(os.path.join(_HERE, "..", ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont

from apps.settings.settings_window import SettingsWindow


def main() -> None:
    app = QApplication(sys.argv)

    # Global font
    font = QFont("Inter", 11)
    font.setHintingPreference(QFont.HintingPreference.PreferNoHinting)
    app.setFont(font)

    # Dark palette at the application level
    app.setStyleSheet("""
        * {
            color: #c0caf5;
            font-family: 'Inter', 'Segoe UI', sans-serif;
        }
    """)

    window = SettingsWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
