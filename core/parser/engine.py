from abc import ABC, abstractmethod
from typing import Any

from playwright.async_api import Page
from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from selenium.webdriver.chrome.webdriver import WebDriver


class BaseScraperEngine(ABC):
    @property
    @abstractmethod
    def native_driver(self) -> Any:
        """Повертає оригінальний драйвер (Page для Playwright, WebDriver для Selenium)"""
        pass

    @abstractmethod
    async def get_text(self, locator: str) -> str | None:
        pass


class PlaywrightEngine(BaseScraperEngine):
    def __init__(self, page: Page):
        self._page = page

    @property
    def native_driver(self) -> Page:
        return self._page

    async def get_text(self, locator: str) -> str | None:
        try:
            element = self._page.locator(locator).first
            return await element.inner_text(timeout=2000)
        except PlaywrightTimeoutError:
            return None
        except Exception as e:
            print(f"Неочікувана помилка при пошуку {locator}: {e}")
            return None


class SeleniumEngine(BaseScraperEngine):
    def __init__(self, driver: WebDriver):
        self._driver = driver

    @property
    def native_driver(self) -> WebDriver:
        return self._driver

    async def get_text(self, locator: str) -> str | None:
        pass
        # webdriver.Chrome()

