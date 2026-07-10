from PyQt6.QtWidgets import QFrame

from PyQt6.QtCore import (
    pyqtSignal,
    Qt,
)

from PyQt6.QtGui import (
    QPainter,
    QPen,
    QColor,
)


class Panel(QFrame):

    clicked = pyqtSignal()

    def __init__(
        self,
        maaya,
        show_border=True
    ):

        super().__init__()

        self.maaya = maaya

        self.palette = self.maaya.theme.Palette

        self.borders = self.maaya.theme.Borders

        # Whether this panel should render a border.
        # Some UI elements (e.g. Header child widgets)
        # participate in the focus system but intentionally
        # remain borderless.
        self.show_border = show_border

        self.active = False

        if self.show_border:

            padding = self.content_padding()

        else:

            padding = 0

        self.setContentsMargins(
            padding,
            padding,
            padding,
            padding
        )

        self.update()

    # =========================================
    # Focus State
    # =========================================

    def set_active(self):

        self.active = True

        self.update()

    # =========================================

    def set_inactive(self):

        self.active = False

        self.update()

    # =========================================

    def is_active(self):

        return self.active

    # =========================================
    # Layout Helpers
    # =========================================

    def content_padding(self):

        """
        Returns the padding required to keep child
        widgets inside the panel border.
        """

        return max(
            self.borders.WIDTH,
            self.borders.ACTIVE_WIDTH
        ) + self.borders.PADDING

    # =========================================
    # Appearance
    # =========================================

    def paintEvent(self, event):

        # Let Qt paint the widget first.
        super().paintEvent(event)

        # Borderless panels participate in the focus system
        # but intentionally render no outline.
        if not self.show_border:
            return

        painter = QPainter(self)

        if self.active:

            color = self.palette.ACCENT
            width = self.borders.ACTIVE_WIDTH

        else:

            color = self.palette.SEPARATOR
            width = self.borders.WIDTH

        pen = QPen(
            QColor(color)
        )

        pen.setWidth(width)

        painter.setPen(pen)

        # Draw the border just inside the widget bounds.
        offset = width

        painter.drawRect(
            self.rect().adjusted(
                offset,
                offset,
                -offset,
                -offset
            )
        )

    # =========================================
    # Mouse Interaction
    # =========================================

    def mousePressEvent(self, event):

        if event.button() == Qt.MouseButton.LeftButton:

            self.clicked.emit()

        super().mousePressEvent(event)

    # =========================================
    # Navigation API
    # =========================================

    def move_up(self):
        pass


    def move_down(self):
        pass


    def move_left(self):
        pass


    def move_right(self):
        pass


    def activate(self):
        pass