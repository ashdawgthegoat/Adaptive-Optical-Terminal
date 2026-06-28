from pathlib import Path

from PyQt6.QtCore import (
    QObject,
    QTimer,
    pyqtSignal
)


class AsciiEngine(QObject):

    frame_changed = pyqtSignal(str)

    def __init__(self):

        super().__init__()

        self.frames = []

        self.current_index = 0

        self.fps = 10

        self.timer = QTimer()

        self.timer.timeout.connect(
            self.next_frame
        )

    def load_animation(self, folder):

        self.stop()

        self.frames.clear()

        self.current_index = 0

        folder = Path(folder)

        files = sorted(folder.glob("*.txt"))

        for file in files:

            self.frames.append(
                file.read_text(
                    encoding="utf-8"
                )
            )

        if self.frames:

            self.frame_changed.emit(
                self.frames[0]
            )

    def play(self):

        if not self.frames:
            return

        self.timer.start(
            int(1000 / self.fps)
        )

    def pause(self):

        self.timer.stop()

    def stop(self):

        self.timer.stop()

        self.current_index = 0

        if self.frames:

            self.frame_changed.emit(
                self.frames[0]
            )

    def next_frame(self):

        if not self.frames:
            return

        self.current_index += 1

        if self.current_index >= len(self.frames):

            self.current_index = 0

        self.frame_changed.emit(
            self.frames[
                self.current_index
            ]
        )

    def set_fps(self, fps):

        self.fps = fps

        if self.timer.isActive():

            self.play()

    def current_frame(self):

        if not self.frames:
            return ""

        return self.frames[
            self.current_index
        ]