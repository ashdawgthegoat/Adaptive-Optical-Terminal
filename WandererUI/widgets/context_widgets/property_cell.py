from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QFrame
)

from PyQt6.QtCore import (
    Qt,
    pyqtSignal
)

from PyQt6.QtGui import QFont


class PropertyCell(QFrame):

    activated = pyqtSignal(str)

    def __init__(
        self,
        maaya,
        title,
        value=""
    ):

        super().__init__()

        self.maaya = maaya

        self.palette = self.maaya.theme.Palette
        self.typography = self.maaya.typography()

        self.title_text = title
        
        if isinstance(value, dict):

            self.value_text = str(
                value.get("value", "")
            )

            self.description = str(
                value.get("text", "")
            )

        else:

            self.value_text = str(value)

            self.description = ""

        self.title = QLabel(title)

        self.value = QLabel(
            self.value_text
        )

        self.description_label = QLabel(
            self.description
        )

        self.selected = False

        self.build_ui()

    # ======================================================

    def build_ui(self):

        layout = QVBoxLayout()

        layout.setContentsMargins(
            0,
            0,
            0,
            20
        )

        layout.setSpacing(0)

        font = QFont(
            self.maaya.font["family"],
            self.typography.FOOTER_SIZE
        )

        self.title.setFont(font)

        self.title.setStyleSheet(
            f"color: {self.palette.PRIMARY};"
        )

        self.description_label.setFont(
            QFont(
                self.maaya.font["family"],
                self.typography.FOOTER_SIZE - 1
            )
        )

        self.description_label.setStyleSheet(
            f"color: {self.palette.SECONDARY};"
        )

        self.description_label.setWordWrap(
            True
        )

        self.description_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft
        )

        self.value.setFont(font)

        self.value.setStyleSheet(
            f"color: {self.palette.SECONDARY};"
        )

        self.title.setAlignment(
            Qt.AlignmentFlag.AlignLeft
        )

        self.value.setAlignment(
            Qt.AlignmentFlag.AlignLeft
        )

        layout.addWidget(
            self.title
        )

        layout.addWidget(
            self.value
        )

        layout.addWidget(
            self.description_label
        )

        for widget in (
            self.title,
            self.value,
            self.description_label
        ):

            widget.setAttribute(
                Qt.WidgetAttribute.WA_TransparentForMouseEvents
            )

        self.setLayout(
            layout
        )

        self.set_unselected()

    # ======================================================

    def set_title(
        self,
        title
    ):

        self.title_text = title

        self.title.setText(
            title
        )

    # ======================================================

    def set_value(self, value):

        if isinstance(value, dict):

            self.value_text = str(
                value.get("value", "")
            )

            self.description = value.get(
                "text",
                ""
            )

        else:

            self.value_text = str(value)

            self.description = ""

        self.value.setText(
            self.value_text
        )

        self.description_label.setText(
            self.description
        )

    # ======================================================

    def set_selected(self):

        self.selected = True

        self.title.setText(
            f">  {self.title_text}"
        )

        self.setStyleSheet(
            f"""
            QWidget {{
                background-color: {self.palette.SURFACE};
            }}
            """
        )

        self.title.setStyleSheet(
            f"color: {self.palette.PRIMARY};"
        )

        self.value.setStyleSheet(
            f"color: {self.palette.PRIMARY};"
        )

        self.description_label.setStyleSheet(
            f"color: {self.palette.PRIMARY};"
        )

    # ======================================================

    def set_unselected(self):

        self.selected = False

        self.title.setText(
            f"   {self.title_text}"
        )

        self.setStyleSheet(
            "background: transparent;"
        )

        self.title.setStyleSheet(
            f"color: {self.palette.PRIMARY};"
        )

        self.value.setStyleSheet(
            f"color: {self.palette.SECONDARY};"
        )

        self.description_label.setStyleSheet(
            f"color: {self.palette.SECONDARY};"
        )

    # ======================================================

    def refresh_presentation(self):

        self.palette = self.maaya.theme.Palette

        self.typography = self.maaya.typography()

        font = QFont(
            self.maaya.font["family"],
            self.typography.FOOTER_SIZE
        )

        self.title.setFont(font)

        self.value.setFont(font)

        self.description_label.setFont(
            QFont(
                self.maaya.font["family"],
                self.typography.FOOTER_SIZE - 1
            )
        )

        if self.selected:

            self.set_selected()

        else:

            self.set_unselected()

        self.update()

    def mousePressEvent(
        self,
        event
    ):

        if event.button() == Qt.MouseButton.LeftButton:

            self.activated.emit(
                self.title_text
            )

        super().mousePressEvent(
            event
        )