from services.ascii_loader import load_ascii


class ViewportManager:

    def __init__(self, viewport):

        self.viewport = viewport

    def show_static(self, name):

        ascii_art = load_ascii(name)

        self.viewport.show_ascii(
            ascii_art
        )

    def show_animation(
        self,
        folder,
        fps=10
    ):

        self.viewport.play_animation(
            folder,
            fps
        )

    def stop_animation(self):

        self.viewport.engine.stop()

    def clear(self):

        self.viewport.clear()