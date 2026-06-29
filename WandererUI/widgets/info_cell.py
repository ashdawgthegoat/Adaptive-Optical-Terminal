from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout
)

from PyQt6.QtCore import Qt, pyqtSignal

from widgets.theme import (
    PRIMARY,
    SECONDARY,
    SMALL_FONT
)

from services.maaya import Maaya


class InfoCell(QWidget):

    activated = pyqtSignal(str, str)

    def __init__(
        self,
        title,
        value="",
        icon=None
    ):

        super().__init__()

        self.maaya = Maaya()

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

        self.title.setFont(
            SMALL_FONT
        )

        self.title.setStyleSheet(
            f"color: {PRIMARY};"
        )

        self.title.setAlignment(
            Qt.AlignmentFlag.AlignLeft
        )

        self.icon.setFont(
            SMALL_FONT
        )

        self.icon.setStyleSheet(
            f"color: {PRIMARY};"
        )

        self.icon.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.value.setFont(
            SMALL_FONT
        )

        self.value.setStyleSheet(
            f"color: {SECONDARY};"
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

    def set_title(self, title):

        self.title_text = title

        self.title.setText(title)

    # =========================================

    def set_value(self, value):

        self.value_text = str(value)

        self.value.setText(
            str(value)
        )

    # =========================================

    def set_icon(self, icon_name):

        self.icon.setText(

            self.maaya.get_icon(
                icon_name
            )

        )

    # =========================================

    def clear_icon(self):

        self.icon.clear()

    def mousePressEvent(self, event):

        if event.button() == Qt.MouseButton.LeftButton:

            self.activated.emit(
                self.title_text,
                self.value_text
        )

        super().mousePressEvent(event)