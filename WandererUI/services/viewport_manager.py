class ViewportManager:

    def __init__(self, viewport):

        self.viewport = viewport

    def show_wallpaper(self):

        self.viewport.show_wallpaper()

    def show_animation(
        self,
        package,
        fps=10
    ):

        self.viewport.play_animation(
            package,
            fps
        )

    def stop_animation(self):

        self.viewport.maaya.stop()

    def clear(self):

        self.viewport.clear()