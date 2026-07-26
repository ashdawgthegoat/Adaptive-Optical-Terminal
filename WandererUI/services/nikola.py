from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt6.QtDBus import (
    QDBusConnection,
    QDBusInterface,
    QDBusVariant,
)


class Nikola(QObject):
    """
    Wanderer's system connectivity service.

    Nikola provides a clean interface between WandererUI and the
    host operating system's NetworkManager service.

    v0.1 is deliberately read-only.
    """

    wifi_state_changed = pyqtSignal(bool)
    network_changed = pyqtSignal(object)

    SERVICE = "org.freedesktop.NetworkManager"

    MANAGER_PATH = "/org/freedesktop/NetworkManager"

    MANAGER_INTERFACE = (
        "org.freedesktop.NetworkManager"
    )

    DEVICE_INTERFACE = (
        "org.freedesktop.NetworkManager.Device"
    )

    WIRELESS_INTERFACE = (
        "org.freedesktop.NetworkManager.Device.Wireless"
    )

    ACCESS_POINT_INTERFACE = (
        "org.freedesktop.NetworkManager.AccessPoint"
    )

    PROPERTIES_INTERFACE = (
        "org.freedesktop.DBus.Properties"
    )

    WIFI_DEVICE_TYPE = 2

    def __init__(self):

        super().__init__()

        self.bus = QDBusConnection.systemBus()

        #self._connect_signals()

    # ============================================================
    # NetworkManager signals
    # ============================================================

    def _connect_signals(self):

        device_path = self._wifi_device()

        if device_path is None:
            return

        connected = self.bus.connect(
            self.SERVICE,
            device_path,
            self.DEVICE_INTERFACE,
            "StateChanged",
            self._device_state_changed
        )

        if not connected:
            print(
                "[Nikola] Failed to subscribe to "
                "Wi-Fi device state changes."
            )

    @pyqtSlot(int, int, int)
    def _device_state_changed(
        self,
        new_state,
        old_state,
        reason
    ):

        self.wifi_state_changed.emit(
            self.wifi_enabled()
        )

        self.network_changed.emit(
            self.current_network()
        )

    # ============================================================
    # Public API
    # ============================================================

    def wifi_enabled(self) -> bool:
        """
        Return whether NetworkManager's Wi-Fi radio is enabled.
        """

        value = self._get_property(
            self.MANAGER_PATH,
            self.MANAGER_INTERFACE,
            "WirelessEnabled"
        )

        return bool(value)

    def set_wifi_enabled(
        self,
        enabled: bool
    ) -> bool:
        """
        Enable or disable Wi-Fi through NetworkManager.

        Returns True when NetworkManager accepts the change.
        """

        properties = self._interface(
            self.MANAGER_PATH,
            self.PROPERTIES_INTERFACE
        )

        if not properties.isValid():

            print(
                "[Nikola] Invalid NetworkManager "
                "properties interface"
            )

            return False

        reply = properties.call(
            "Set",
            self.MANAGER_INTERFACE,
            "WirelessEnabled",
            QDBusVariant(
                bool(enabled)
            )
        )

        if reply.type() == reply.MessageType.ErrorMessage:

            print(
                "[Nikola] Failed to set Wi-Fi state:",
                reply.errorMessage()
            )

            return False

        return True

    def current_network(self) -> str | None:
        """
        Return the SSID of the currently active Wi-Fi network.

        Returns None when no Wi-Fi network is active.
        """

        device_path = self._wifi_device()

        if device_path is None:
            return None

        access_point_path = self._get_property(
            device_path,
            self.WIRELESS_INTERFACE,
            "ActiveAccessPoint"
        )

        if not access_point_path:
            return None

        access_point_path = str(
            access_point_path
        )

        if access_point_path == "/":
            return None

        ssid = self._get_property(
            access_point_path,
            self.ACCESS_POINT_INTERFACE,
            "Ssid"
        )

        return self._decode_ssid(
            ssid
        )

    def available_networks(self) -> list[dict]:
        """
        Return visible Wi-Fi networks.

        Multiple access points broadcasting the same SSID are collapsed
        into a single Wanderer-facing network entry. The strongest access
        point is retained.
        """

        device_path = self._wifi_device()

        if device_path is None:
            return []

        reply = self._call(
            device_path,
            self.WIRELESS_INTERFACE,
            "GetAccessPoints"
        )

        if reply is None:
            return []

        arguments = reply.arguments()

        if not arguments:
            return []

        access_points = arguments[0]

        current = self.current_network()

        networks: dict[str, dict] = {}

        for access_point_path in access_points:

            access_point_path = str(
                access_point_path
            )

            ssid = self._decode_ssid(
                self._get_property(
                    access_point_path,
                    self.ACCESS_POINT_INTERFACE,
                    "Ssid"
                )
            )

            if not ssid:
                continue

            strength = self._get_property(
                access_point_path,
                self.ACCESS_POINT_INTERFACE,
                "Strength"
            )

            flags = self._get_property(
                access_point_path,
                self.ACCESS_POINT_INTERFACE,
                "Flags"
            )

            wpa_flags = self._get_property(
                access_point_path,
                self.ACCESS_POINT_INTERFACE,
                "WpaFlags"
            )

            rsn_flags = self._get_property(
                access_point_path,
                self.ACCESS_POINT_INTERFACE,
                "RsnFlags"
            )

            strength = self._decode_byte(
                strength
            )

            flags = int(
                flags or 0
            )

            wpa_flags = int(
                wpa_flags or 0
            )

            rsn_flags = int(
                rsn_flags or 0
            )

            secured = bool(
                flags
                or wpa_flags
                or rsn_flags
            )

            network = {
                "ssid": ssid,
                "strength": strength,
                "secured": secured,
                "connected": ssid == current,
            }

            existing = networks.get(
                ssid
            )

            if (
                existing is None
                or strength > existing["strength"]
            ):
                networks[ssid] = network

        return sorted(
            networks.values(),
            key=lambda network: (
                not network["connected"],
                -network["strength"],
                network["ssid"].lower()
            )
        )

    # ============================================================
    # NetworkManager discovery
    # ============================================================

    def _wifi_device(self) -> str | None:
        """
        Return the first NetworkManager Wi-Fi device object path.
        """

        reply = self._call(
            self.MANAGER_PATH,
            self.MANAGER_INTERFACE,
            "GetDevices"
        )

        if reply is None:
            return None

        arguments = reply.arguments()

        if not arguments:
            return None

        devices = arguments[0]

        for device_path in devices:

            device_path = str(
                device_path
            )

            device_type = self._get_property(
                device_path,
                self.DEVICE_INTERFACE,
                "DeviceType"
            )

            if device_type is None:
                continue

            if int(device_type) == self.WIFI_DEVICE_TYPE:
                return device_path

        return None

    # ============================================================
    # D-Bus helpers
    # ============================================================

    def _interface(
        self,
        path: str,
        interface: str
    ) -> QDBusInterface:

        return QDBusInterface(
            self.SERVICE,
            path,
            interface,
            self.bus
        )

    def _call(
        self,
        path: str,
        interface: str,
        method: str,
        *arguments
    ):
        """
        Perform a synchronous read-only D-Bus method call.
        """

        dbus_interface = self._interface(
            path,
            interface
        )

        if not dbus_interface.isValid():

            print(
                "[Nikola] Invalid D-Bus interface:",
                interface,
                path
            )

            return None

        reply = dbus_interface.call(
            method,
            *arguments
        )

        if reply.type() == reply.MessageType.ErrorMessage:

            print(
                "[Nikola] D-Bus call failed:",
                method,
                reply.errorMessage()
            )

            return None

        return reply

    def _get_property(
        self,
        path: str,
        interface: str,
        property_name: str
    ):
        """
        Read one D-Bus property.
        """

        properties = self._interface(
            path,
            self.PROPERTIES_INTERFACE
        )

        if not properties.isValid():

            print(
                "[Nikola] Invalid properties interface:",
                path
            )

            return None

        reply = properties.call(
            "Get",
            interface,
            property_name
        )

        if reply.type() == reply.MessageType.ErrorMessage:

            print(
                "[Nikola] Failed to read property:",
                property_name,
                reply.errorMessage()
            )

            return None

        arguments = reply.arguments()

        if not arguments:
            return None

        value = arguments[0]

        # PyQt may return a QDBusVariant for Properties.Get().
        if hasattr(value, "variant"):
            value = value.variant()

        return value

    # ============================================================
    # Data conversion
    # ============================================================

    def _decode_byte(
        self,
        value
    ) -> int:
        """
        Convert a D-Bus BYTE value into a Python integer.
        """

        if value is None:
            return 0

        if isinstance(
            value,
            bytes
        ):

            if not value:
                return 0

            return value[0]

        if isinstance(
            value,
            bytearray
        ):

            if not value:
                return 0

            return value[0]

        return int(value)

    def _decode_ssid(
        self,
        value
    ) -> str | None:
        """
        Convert NetworkManager's SSID byte array into text.
        """

        if value is None:
            return None

        if hasattr(value, "data"):
            value = value.data()

        try:

            raw = bytes(
                value
            )

        except (TypeError, ValueError):

            return None

        if not raw:
            return None

        return raw.decode(
            "utf-8",
            errors="replace"
        )