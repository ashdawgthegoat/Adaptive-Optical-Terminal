from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout
)

from PyQt6.QtCore import (
    Qt,
    pyqtSignal
)

from PyQt6.QtGui import QFont


class InfoCell(QWidget):

    activated = pyqtSignal(str, str)

    def __init__(
        self,
        maaya,
        title,
        value="",
        icon=None
    ):

        super().__init__()

        self.maaya = maaya

        self.palette = self.maaya.theme.Palette

        self.typography = self.maaya.typography()

        self.title_text = title

        self.value_text = str(value)

        self.title = QLabel(title)

        self.icon = QLabel()

        self.value = QLabel(str(value))

        self.build_ui()

        if icon:

            self.set_icon(icon)

    # =========================================

    def build_ui(self):

        layout = QVBoxLayout()

        layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        layout.setSpacing(2)

        font = QFont(
            self.maaya.font["family"],
            self.typography.FOOTER_SIZE
        )

        self.title.setFont(font)

        self.title.setStyleSheet(
            f"color: {self.palette.PRIMARY};"
        )

        self.title.setAlignment(
            Qt.AlignmentFlag.AlignLeft
        )

        self.icon.setFont(font)

        self.icon.setStyleSheet(
            f"color: {self.palette.PRIMARY};"
        )

        self.icon.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.value.setFont(font)

        self.value.setStyleSheet(
            f"color: {self.palette.SECONDARY};"
        )

        self.value.setAlignment(
            Qt.AlignmentFlag.AlignLeft
        )

        layout.addWidget(self.title)
        layout.addWidget(self.icon)
        layout.addWidget(self.value)

        for widget in (
            self.title,
            self.icon,
            self.value
        ):

            widget.setAttribute(
                Qt.WidgetAttribute.WA_TransparentForMouseEvents
            )

        self.setLayout(layout)

    # =========================================

    def set_title(
        self,
        title
    ):

        self.title_text = title

        self.title.setText(title)

    # =========================================

    def set_value(
        self,
        value
    ):

        self.value_text = str(value)

        self.value.setText(
            str(value)
        )

    # =========================================

    def set_icon(
        self,
        glyph
    ):

        self.icon.setText(
            glyph
        )

    # =========================================

    def clear_icon(self):

        self.icon.clear()

    # =========================================

    def mousePressEvent(
        self,
        event
    ):

        if event.button() == Qt.MouseButton.LeftButton:

            self.activated.emit(
                self.title_text,
                self.value_text
            )

        super().mousePressEvent(
            event
        )