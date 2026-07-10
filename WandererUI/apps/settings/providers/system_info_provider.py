import platform
import shutil

import psutil


# ==========================================================
# System Info Provider
#
# Reads live system information for display on the About
# page. All methods return plain strings suitable for
# direct rendering.
# ==========================================================


class SystemInfoProvider:

    # ======================================================
    # Identity
    # ======================================================

    def hostname(self) -> str:
        """
        Returns the system hostname.
        """

        return platform.node()

    # ======================================================

    def platform_name(self) -> str:
        """
        Returns the platform name and kernel release.
        """

        return f"{platform.system()} {platform.release()}"

    # ======================================================
    # Resource Usage
    # ======================================================

    def cpu_usage(self) -> str:
        """
        Returns the current CPU usage percentage.
        """

        percent = psutil.cpu_percent(interval=None)

        return f"{percent}%"

    # ======================================================

    def memory_usage(self) -> str:
        """
        Returns memory usage as used / total in GB.
        """

        mem = psutil.virtual_memory()

        used_gb = mem.used / (1024 ** 3)
        total_gb = mem.total / (1024 ** 3)

        return f"{used_gb:.1f} / {total_gb:.1f} GB"

    # ======================================================

    def storage_usage(self) -> str:
        """
        Returns disk usage for / as used / total in GB.
        """

        usage = shutil.disk_usage("/")

        used_gb = usage.used / (1024 ** 3)
        total_gb = usage.total / (1024 ** 3)

        return f"{used_gb:.0f} / {total_gb:.0f} GB"

    # ======================================================
    # Battery
    # ======================================================

    def battery_status(self) -> str:
        """
        Returns the battery percentage or "N/A" if no
        battery is present.
        """

        battery = psutil.sensors_battery()

        if battery is None:

            return "N/A"

        return f"{battery.percent}%"
