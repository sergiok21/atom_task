from playwright.async_api import Page

from core.parser.base import TextField, XPathLocator
from utils.waiter import async_sleep_after


class BaseAction:
    def __init__(self, page: "Page"):
        self.page = page


class SearchFieldAction(BaseAction):
    @async_sleep_after()
    async def fill_and_send(self, locator: str = XPathLocator.search_field, text: str = TextField.search_text) -> None:
        search_field = self.page.locator(locator).last
        await search_field.fill(text, timeout=2000)
        await search_field.press('Enter')


class ButtonAction(BaseAction):
    @async_sleep_after()
    async def click(self, locator: str = XPathLocator.element_from_grid) -> None:
        first_element = self.page.locator(locator).first
        await first_element.click()
