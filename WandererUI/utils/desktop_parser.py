from configparser import ConfigParser
from pathlib import Path


class DesktopParser:

    @staticmethod
    def parse(path):

        path = Path(path)

        if not path.exists():
            return None

        parser = ConfigParser(interpolation=None)

        try:
            parser.read(path, encoding="utf-8")
        except Exception:
            return None

        if "Desktop Entry" not in parser:
            return None

        entry = parser["Desktop Entry"]

        if "Name" not in entry or "Exec" not in entry:
            return None

        return {
            "id": path.stem,
            "name": entry["Name"],
            "exec": entry["Exec"],
            "icon": entry.get("Icon", ""),
            "comment": entry.get("Comment", ""),
            "categories": entry.get("Categories", ""),
            "terminal": entry.getboolean("Terminal", fallback=False),
            "native": entry.getboolean(
                "X-Wanderer-Native",
                fallback=False
            ),
            "path": str(path)
        }