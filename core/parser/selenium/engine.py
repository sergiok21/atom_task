from selenium.common import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from core.parser.meta.engine import BaseScraperEngine


class SeleniumEngine(BaseScraperEngine):
    def __init__(self, driver: WebDriver):
        self._driver = driver

    @property
    def native_driver(self) -> WebDriver:
        return self._driver

    async def get_text(self, locator: str) -> str | None:
        try:
            wait = WebDriverWait(self._driver, 2)
            element = wait.until(EC.presence_of_element_located((By.XPATH, locator)))
            text = element.get_attribute("textContent")
            return text.strip() if text else None
        except TimeoutException:
            return None
        except Exception as e:
            print(f"Неочікувана помилка при пошуку {locator}: {e}")
            return None
