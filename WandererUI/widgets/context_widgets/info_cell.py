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
        data=None,
        icon=None
    ):

        super().__init__()

        self.maaya = maaya

        self.palette = self.maaya.theme.Palette

        self.typography = self.maaya.typography()

        self.title_text = title

        self.data = data or {
            "value": None,
            "text": ""
        }

        self.title = QLabel(title)

        self.icon = QLabel()

        self.value = QLabel(
            self.render_text()
        )

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

        if self.icon.text():
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

    def set_data(
        self,
        data
    ):

        self.data = data

        self.value.setText(
            self.render_text()
        )

    # =========================================

    def render_text(self):

        style = self.maaya.theme.Information.STYLE

        text = self.data["text"]

        value = self.data["value"]

        if style == "text" or value is None:
            return text

        length = self.maaya.theme.Information.BAR_LENGTH

        filled = self.maaya.theme.Information.FILLED

        empty = self.maaya.theme.Information.EMPTY

        blocks = round((value / 100) * length)

        bar = (
            filled * blocks
            + empty * (length - blocks)
        )

        return f"{bar} {text}"

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

    def refresh_presentation(self):

        self.palette = self.maaya.theme.Palette

        self.typography = self.maaya.typography()

        font = QFont(
            self.maaya.font["family"],
            self.typography.FOOTER_SIZE
        )

        self.title.setFont(font)

        self.icon.setFont(font)

        self.value.setFont(font)

        self.title.setStyleSheet(
            f"color: {self.palette.PRIMARY};"
        )

        self.icon.setStyleSheet(
            f"color: {self.palette.PRIMARY};"
        )

        self.value.setStyleSheet(
            f"color: {self.palette.SECONDARY};"
        )

        self.value.setText(
            self.render_text()
        )

        self.update()

    def mousePressEvent(
        self,
        event
    ):

        if event.button() == Qt.MouseButton.LeftButton:

            self.activated.emit(
                self.title_text,
                self.data["text"]
            )

        super().mousePressEvent(
            event
        )