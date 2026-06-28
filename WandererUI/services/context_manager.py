from services.system_info import SystemInfo
from PyQt6.QtCore import QTimer


class ContextManager:

    def __init__(self, context):

        self.context = context

        self.timer = QTimer()

        self.timer.timeout.connect(
            self.refresh_system
        )
    
    def start(self, interval=1000):

        self.refresh_system()

        self.timer.start(interval)


    def stop(self):

        self.timer.stop()

    def refresh_system(self):

        self.context.set_title(
            "SYSTEM STATUS"
        )

        self.context.set_info({

            "CPU":
                SystemInfo.cpu(),

            "Memory":
                SystemInfo.memory(),

            "Storage":
                SystemInfo.storage(),

            "Battery":
                SystemInfo.battery(),

            "Status":
                SystemInfo.status()

        })

    def destroy(self):

        self.stop()

    def show_module(
        self,
        info
    ):

        self.context.set_title(
            "MODULE STATUS"
        )

        self.context.set_info(
            info
        )

    def clear(self):

        self.context.set_info({})