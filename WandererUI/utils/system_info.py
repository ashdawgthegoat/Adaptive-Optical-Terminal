import shutil
import platform
from datetime import datetime

import psutil


class SystemInfo:

    @staticmethod
    def cpu():

        return f"{psutil.cpu_percent(interval=None)} %"

    @staticmethod
    def memory():

        memory = psutil.virtual_memory()

        used = memory.used / (1024 ** 3)

        total = memory.total / (1024 ** 3)

        return f"{used:.1f} / {total:.1f} GB"

    @staticmethod
    def storage():

        disk = shutil.disk_usage("/")

        free = disk.free / (1024 ** 3)

        return f"{free:.0f} GB Free"

    @staticmethod
    def battery():

        battery = psutil.sensors_battery()

        if battery is None:

            return "N/A"

        return f"{battery.percent:.0f}%"

    @staticmethod
    def hostname():

        return platform.node()

    @staticmethod
    def time():

        return datetime.now().strftime(
            "%H:%M:%S"
        )

    @staticmethod
    def status():

        return "Ready"