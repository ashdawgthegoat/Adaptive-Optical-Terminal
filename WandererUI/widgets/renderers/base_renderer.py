from PyQt6.QtWidgets import QWidget


class BaseRenderer(QWidget):

    def show_content(self, content):

        raise NotImplementedError


    def clear(self):

        raise NotImplementedError