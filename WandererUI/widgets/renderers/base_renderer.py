from PyQt6.QtWidgets import QWidget


class BaseRenderer(QWidget):

    def __init__(self):

        super().__init__()

    def show_content(self, content):

        raise NotImplementedError

    def update_display(self):

        raise NotImplementedError

    def clear(self):

        raise NotImplementedError