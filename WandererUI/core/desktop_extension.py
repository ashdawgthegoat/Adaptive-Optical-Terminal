from abc import ABC, abstractmethod


class DesktopApplication(ABC):
    """
    Base contract for every Desktop Core application.

    A Desktop Application extends the Desktop rather than
    replacing it. The Desktop owns the shell, while the
    application provides the content.
    """

    @abstractmethod
    def name(self) -> str:
        """Application name."""
        raise NotImplementedError

    @abstractmethod
    def navigation_items(self) -> list[str]:
        """Items shown in the Navigation Panel."""
        raise NotImplementedError

    @abstractmethod
    def context(self):
        """Content displayed inside the Context Panel."""
        raise NotImplementedError

    def context_title(self) -> str:
        """Title displayed by the Context Panel."""
        return "CONTEXT"

    @abstractmethod
    def viewport(self):
        """Content displayed inside the Viewport."""
        raise NotImplementedError

    def viewport_title(self) -> str:
        """
        Title displayed by the Desktop's
        Viewport panel.
        """

        return "Viewport"

    @abstractmethod
    def footer_hints(self) -> str:
        """Keyboard hints shown in the Footer."""
        raise NotImplementedError

    def on_enter(self) -> None:
        """Called when the application becomes active."""
        pass

    def on_leave(self) -> None:
        """Called before the application is closed."""
        pass