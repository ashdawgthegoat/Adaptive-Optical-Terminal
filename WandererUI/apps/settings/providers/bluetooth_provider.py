# ==========================================================
# Bluetooth Provider
#
# Stub provider for Bluetooth device discovery.
# ==========================================================


class BluetoothProvider:

    # ======================================================
    # Device Discovery
    # ======================================================

    def list_devices(self) -> list[str]:
        """
        Returns a list of available Bluetooth devices.
        """

        # TODO: Implement Bluetooth device scanning via
        #       BlueZ / D-Bus.

        return []
