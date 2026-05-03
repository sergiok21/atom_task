from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from core.parser.meta.property import XPathLocator, TextField
from core.parser.meta.action import BaseSearchFieldAction, BaseButtonAction
from utils.waiter import async_sleep_after


class SeleniumAction:
    def __init__(self, driver: WebDriver):
        self.driver = driver


class SearchFieldActionSelenium(BaseSearchFieldAction, SeleniumAction):
    @async_sleep_after()
    async def fill_and_send(self, locator: str = XPathLocator.search_field, text: str = TextField.search_text) -> None:
        wait = WebDriverWait(self.driver, 2)
        search_field = wait.until(EC.element_to_be_clickable((By.XPATH, locator)))

        search_field.clear()
        search_field.send_keys(text)
        search_field.send_keys(Keys.ENTER)


class ButtonActionSelenium(BaseButtonAction, SeleniumAction):
    @async_sleep_after()
    async def click(self, locator: str = XPathLocator.element_from_grid) -> None:
        wait = WebDriverWait(self.driver, 2)
        first_element = wait.until(EC.element_to_be_clickable((By.XPATH, locator)))
        first_element.click()
