class Kaizen:

    def __init__(self):

        self.regions = []

        self.current_index = 0

    # ==========================================
    # Registration
    # ==========================================

    def register(self, name):

        if name not in self.regions:

            self.regions.append(name)

    # ==========================================
    # Startup
    # ==========================================

    def initialize(self):

        if "navigation" in self.regions:

            self.current_index = self.regions.index(
                "navigation"
            )

        else:

            self.current_index = 0

    # ==========================================
    # Focus
    # ==========================================

    def current(self):

        if not self.regions:

            return None

        return self.regions[
            self.current_index
        ]

    def set_focus(self, name):

        if name in self.regions:

            self.current_index = self.regions.index(
                name
            )

    def has_focus(self, name):

        return self.current() == name

    # ==========================================
    # Navigation
    # ==========================================

    def next(self):

        if not self.regions:

            return None

        self.current_index += 1

        if self.current_index >= len(self.regions):

            self.current_index = 0

        return self.current()

    def previous(self):

        if not self.regions:

            return None

        self.current_index -= 1

        if self.current_index < 0:

            self.current_index = len(
                self.regions
            ) - 1

        return self.current()

    # ==========================================
    # Utilities
    # ==========================================

    def reset(self):

        self.current_index = 0

        self.initialize()

    def count(self):

        return len(
            self.regions
        )

    def registered_regions(self):

        return self.regions.copy()