# ==========================================================
# Network Provider
#
# Stub provider for Wi-Fi network discovery.
# ==========================================================


class NetworkProvider:

    # ======================================================
    # Network Discovery
    # ======================================================

    def list_networks(self) -> list[str]:
        """
        Returns a list of available Wi-Fi networks.
        """

        # TODO: Implement Wi-Fi network scanning via
        #       NetworkManager or nmcli.

        return []
