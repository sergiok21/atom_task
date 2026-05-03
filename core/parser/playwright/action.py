from playwright.async_api import Page

from core.parser.property import XPathLocator, TextField
from core.parser.base_action import BaseSearchFieldAction, BaseButtonAction
from utils.waiter import async_sleep_after


class PlaywrightAction:
    def __init__(self, page: "Page"):
        self.page = page


class SearchFieldActionPlaywright(BaseSearchFieldAction, PlaywrightAction):
    @async_sleep_after()
    async def fill_and_send(self, locator: str = XPathLocator.search_field, text: str = TextField.search_text) -> None:
        search_field = self.page.locator(locator)
        await search_field.fill(text, timeout=2000)
        await search_field.press('Enter')


class ButtonActionPlaywright(BaseButtonAction, PlaywrightAction):
    @async_sleep_after()
    async def click(self, locator: str = XPathLocator.element_from_grid) -> None:
        first_element = self.page.locator(locator).first
        await first_element.click()
