from abc import ABC, abstractmethod
from typing import Any


class BaseScraperEngine(ABC):
    """Abstract base class defining the core interface for scraper engines."""

    @property
    @abstractmethod
    def native_driver(self) -> Any:
        """Returns the underlying driver instance (e.g., Page, WebDriver, Soup)."""
        pass

    @abstractmethod
    async def get_text(self, locator: str) -> str | None:
        """Retrieves text content from an element identified by the locator.

        Args:
            locator: The element identifier string.

        Returns:
            The extracted text or None if the element is not found.
        """
        pass
