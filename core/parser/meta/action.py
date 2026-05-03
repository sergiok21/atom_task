from abc import ABC, abstractmethod


class BaseSearchFieldAction(ABC):
    """Abstract base class defining actions for search input fields."""

    @abstractmethod
    async def fill_and_send(self, locator: str, text: str) -> None:
        """Fills the search field with text and submits the query.

        Args:
            locator: The element identifier string.
            text: The search query string.
        """
        ...


class BaseButtonAction(ABC):
    """Abstract base class defining click actions for buttons."""

    @abstractmethod
    async def click(self, locator: str) -> None:
        """Performs a click operation on the specified element.

        Args:
            locator: The element identifier string.
        """
        ...