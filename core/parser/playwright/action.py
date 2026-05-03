from playwright.async_api import Page
from core.parser.meta.property import XPathLocator, TextField
from core.parser.meta.action import BaseSearchFieldAction, BaseButtonAction
from utils.waiter import async_sleep_after


class PlaywrightAction:
    """Base class for Playwright-based actions requiring a Page instance."""
    def __init__(self, page: Page):
        """Initializes the action with a Playwright Page object."""
        self.page = page


class SearchFieldActionPlaywright(BaseSearchFieldAction, PlaywrightAction):
    """Implementation of search field interactions using Playwright."""
    @async_sleep_after()
    async def fill_and_send(self, locator: str = XPathLocator.search_field, text: str = TextField.search_text) -> None:
        """Locates the search input, fills it with text, and presses Enter."""
        search_field = self.page.locator(locator)
        await search_field.fill(text, timeout=2000)
        await search_field.press('Enter')


class ButtonActionPlaywright(BaseButtonAction, PlaywrightAction):
    """Implementation of button click interactions using Playwright."""
    @async_sleep_after()
    async def click(self, locator: str = XPathLocator.element_from_grid) -> None:
        """Locates the first matching element and performs a click."""
        first_element = self.page.locator(locator).first
        await first_element.click()
