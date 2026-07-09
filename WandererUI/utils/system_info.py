import shutil
import platform
from datetime import datetime

import psutil


class SystemInfo:

    @staticmethod
    def metric(value=None, text=""):

        return {
            "value": value,
            "text": text,
        }

    @staticmethod
    def cpu():

        value = psutil.cpu_percent(interval=None)

        return SystemInfo.metric(
            value=value,
            text=f"{value:.0f}%"
        )

    @staticmethod
    def memory():

        memory = psutil.virtual_memory()

        used = memory.used / (1024 ** 3)

        total = memory.total / (1024 ** 3)

        return SystemInfo.metric(
            value=memory.percent,
            text=f"{used:.1f} / {total:.1f} GB"
        )

    @staticmethod
    def storage():

        disk = shutil.disk_usage("/")

        used_percent = (
            (disk.used / disk.total) * 100
        )

        return SystemInfo.metric(
            value=used_percent,
            text=f"{used_percent:.0f} GB Free"
        )

    @staticmethod
    def battery():

        battery = psutil.sensors_battery()

        if battery is None:

            return SystemInfo.metric(
                text="N/A"
            )

        return SystemInfo.metric(
            value=battery.percent,
            text=f"{battery.percent:.0f}%"
        )

    @staticmethod
    def hostname():

        return SystemInfo.metric(
            text=platform.node()
        )

    @staticmethod
    def time():

        return datetime.now().strftime(
            "%H:%M:%S"
        )

    @staticmethod
    def status():

        return SystemInfo.metric(
            text="Ready"
        )