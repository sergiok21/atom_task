from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError

from core.parser.meta.engine import BaseScraperEngine


class PlaywrightEngine(BaseScraperEngine):
    """Playwright-based implementation of the scraping engine."""

    def __init__(self, page: Page):
        """Initializes the engine with a Playwright Page instance."""
        self._page = page

    @property
    def native_driver(self) -> Page:
        """Returns the underlying Playwright Page object."""
        return self._page

    async def get_text(self, locator: str) -> str | None:
        """Retrieves inner text from the first element matching the locator.

        Returns:
            The text content or None if a timeout or error occurs.
        """
        try:
            element = self._page.locator(locator).first
            return await element.inner_text(timeout=2000)
        except PlaywrightTimeoutError:
            return None
        except Exception as e:
            print(f"Unexpected error while searching for {locator}: {e}")
            return None