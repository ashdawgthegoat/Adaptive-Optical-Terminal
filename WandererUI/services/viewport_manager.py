class ViewportManager:

    def __init__(self, viewport):

        self.viewport = viewport

    def show_static(self, name):

        self.viewport.show_ascii(
            name
        )

    def show_animation(
        self,
        name,
        fps=10
    ):

        self.viewport.play_animation(
            name,
            fps
        )

    def stop_animation(self):

        self.viewport.maaya.stop()

    def clear(self):

        self.viewport.clear()