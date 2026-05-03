from bs4 import BeautifulSoup

from core.parser.meta.engine import BaseScraperEngine


class BS4Engine(BaseScraperEngine):
    """BeautifulSoup-based implementation of the scraping engine.

    This class provides a concrete implementation of the BaseScraperEngine
    using the BeautifulSoup library for parsing static HTML content.
    """

    def __init__(self, soup: BeautifulSoup):
        """Initializes the engine with a BeautifulSoup object.

        Args:
            soup: A pre-initialized BeautifulSoup instance containing the
                HTML content to be parsed.
        """
        self._soup = soup

    @property
    def native_driver(self) -> BeautifulSoup:
        """Returns the underlying BeautifulSoup instance.

        Returns:
            The BeautifulSoup object used for searching and navigating the HTML.
        """
        return self._soup

    async def get_text(self, locator: str) -> str | None:
        """Extracts text content from an element identified by a CSS selector.

        Args:
            locator: A CSS selector string used to find the target element.

        Returns:
            The stripped text content of the found element, or None if the
            element does not exist or an error occurs.
        """
        try:
            element = self._soup.select_one(locator)
            return element.get_text(strip=True) if element else None
        except Exception as e:
            print(f"Неочікувана помилка при пошуку {locator}: {e}")
            return None
