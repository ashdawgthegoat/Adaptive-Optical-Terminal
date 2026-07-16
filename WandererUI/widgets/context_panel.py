from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QWidget,
    QVBoxLayout,
    QScrollArea
)

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

from widgets.context_widgets.info_cell import InfoCell
from widgets.context_widgets.property_cell import PropertyCell
from widgets.layer.panel import Panel

# ==========================================================
# Context Panel
#
# Displays contextual information related to the currently
# active application or the overall system state.
#
# This panel participates in the focus system and renders
# the standard panel border.
# ==========================================================

class ContextPanel(Panel):

    def __init__(self, maaya):

        super().__init__(
            maaya,
            show_border=True
        )

        self.maaya = maaya

        self.palette = self.maaya.theme.Palette
        self.spacing = self.maaya.theme.Spacing
        self.borders = self.maaya.theme.Borders
        self.typography = self.maaya.typography()

        self.properties = []

        self.current_index = 0

        self.build_ui()

    # ==========================================================
    # UI Construction
    # ==========================================================

    def build_ui(self):

        root_layout = QVBoxLayout()

        padding = self.content_padding()

        root_layout.setContentsMargins(
            padding,    
            padding,
            padding,
            padding
        )

        self.scroll = QScrollArea()

        self.content = QWidget()

        self.main_layout = QVBoxLayout()

        self.main_layout.setContentsMargins(
            10,
            10,
            10,
            10
        )

        self.main_layout.setSpacing(
            self.spacing.ITEM_SPACING
        )

        # ============================
        # SYSTEM SECTION
        # ============================

        self.system_title = QLabel(
            "SYSTEM STATUS"
        )

        self.system_title.setFont(
            QFont(
                self.maaya.font["family"],
                self.typography.SECTION_SIZE
            )
        )

        self.system_title.setStyleSheet(
            f"color: {self.palette.PRIMARY};"
        )

        self.system_title.setAlignment(
            Qt.AlignmentFlag.AlignLeft
        )

        self.main_layout.addWidget(
            self.system_title
        )

        self.system_layout = QVBoxLayout()

        self.content_widget = None

        self.system_layout.setSpacing(0)

        self.main_layout.addLayout(
            self.system_layout,
        )

        self.main_layout.addStretch()

        # ============================
        # DIVIDER
        # ============================

        self.divider = QFrame()

        self.divider.setFrameShape(
            QFrame.Shape.HLine
        )

        self.divider.setFixedHeight(
            self.borders.WIDTH
        )

        self.divider.setStyleSheet(
            f"""
            background-color: {self.palette.ACCENT};
            """
        )

        self.main_layout.addWidget(
            self.divider
        )

        # ============================
        # MODULE PORT
        # ============================

        self.module_title = QLabel(
            "MODULE PORT"
        )

        self.module_title.setFont(
            QFont(
                self.maaya.font["family"],
                self.typography.SECTION_SIZE
            )
        )

        self.module_title.setStyleSheet(
            f"color: {self.palette.PRIMARY};"
        )

        self.main_layout.addWidget(
            self.module_title
        )

        self.module_layout = QVBoxLayout()

        self.module_layout.setSpacing(4)

        self.main_layout.addLayout(
            self.module_layout,
        )

        self.content.setLayout(
            self.main_layout
        )

        self.scroll.setWidget(
            self.content
        )

        self.scroll.setWidgetResizable(
            True
        )

        self.scroll.setFrameShape(
            QScrollArea.Shape.NoFrame
        )

        self.scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        root_layout.addWidget(
            self.scroll
        )

        self.setLayout(
            root_layout
        )

        self.set_module_info({
            "Status": {
                "value": None,
                "text": "No Active Module"
            }
        })

        self.set_inactive()

    def set_content(self, widget):
        """Display a custom widget inside the context panel."""

        self._clear_layout(
            self.system_layout
        )

        self.content_widget = widget

        self.system_layout.addWidget(
            widget
        )

    # ==========================================================
    # Layout Utilities
    # ==========================================================

    def _clear_layout(self, layout):

        while layout.count():

            item = layout.takeAt(0)

            if item.widget():

                item.widget().deleteLater()

    # ==========================================================
    # Context Information
    # ==========================================================

    def set_context(self, info):

        self._clear_layout(
            self.system_layout
        )

        for key, value in info.items():

            cell = InfoCell(
                self.maaya,
                title=key,
                data=value
            )

            self.system_layout.addWidget(
                cell
            )

    def set_properties(self, properties):
        """Display configurable application properties."""

        self.properties.clear()

        self.current_index = 0

        self._clear_layout(
            self.system_layout
        )

        for title, value in properties.items():

            cell = PropertyCell(
                self.maaya,
                title=title,
                value=value
            )

            self.properties.append(
                cell
            )

            self.system_layout.addWidget(
                cell
            )

        if self.properties:

            self.properties[0].set_selected()

        self.system_layout.addStretch()

    # =======================================
    # Navigation
    # =======================================

    def move_up(self):

        if not self.properties:
            return

        self.properties[
            self.current_index
        ].set_unselected()

        self.current_index = max(
            0,
            self.current_index - 1
        )

        self.properties[
            self.current_index
        ].set_selected()

    def move_down(self):

        if not self.properties:
            return

        self.properties[
            self.current_index
        ].set_unselected()

        self.current_index = min(
            len(self.properties) - 1,
            self.current_index + 1
        )

        self.properties[
            self.current_index
        ].set_selected()

    # ====================================

    def current_property(self):

        if not self.properties:
            return None

        return self.properties[
            self.current_index
        ].title_text

    # =====================================

    def activate(self):

        if not self.properties:
            return

        return self.current_property()

    # =====================================

    def set_module_info(self, info):

        self._clear_layout(
            self.module_layout
        )

        for key, value in info.items():

            cell = InfoCell(
                self.maaya,
                title=key,
                data=value
            )

            self.module_layout.addWidget(
                cell
            )

        self.module_layout.addStretch()

    # =====================================

    def set_title(self, title):

        self.system_title.setText(
            title
        )

    def refresh_presentation(self):

        self.palette = self.maaya.theme.Palette

        self.spacing = self.maaya.theme.Spacing

        self.borders = self.maaya.theme.Borders

        self.typography = self.maaya.typography()

        self.system_title.setFont(
            QFont(
                self.maaya.font["family"],
                self.typography.SECTION_SIZE
            )
        )

        self.module_title.setFont(
            QFont(
                self.maaya.font["family"],
                self.typography.SECTION_SIZE
            )
        )

        self.system_title.setStyleSheet(
            f"color: {self.palette.PRIMARY};"
        )

        self.module_title.setStyleSheet(
            f"color: {self.palette.PRIMARY};"
        )

        self.divider.setFixedHeight(
            self.borders.WIDTH
        )

        self.divider.setStyleSheet(
            f"background-color: {self.palette.ACCENT};"
        )

        self.main_layout.setSpacing(
            self.spacing.ITEM_SPACING
        )

        for cell in self.properties:

            cell.refresh_presentation()

        for layout in (
            self.system_layout,
            self.module_layout
        ):

            for i in range(layout.count()):

                item = layout.itemAt(i)

                widget = item.widget()

                if (
                    widget is not None
                    and hasattr(
                        widget,
                        "refresh_presentation"
                    )
                ):

                    widget.refresh_presentation()

        self.update()

    # ==========================================================
    # Reset State
    # ==========================================================

    def clear_module(self):

        self.set_module_info({
            "Status": {
                "value": None,
                "text": "No Active Module"
            }
        })