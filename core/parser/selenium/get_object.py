from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from core.parser.meta.property import ExcludeField
from core.parser.meta.get_object import BaseGetImage, BaseGetDetail


class GetImageSelenium(BaseGetImage):
    async def execute(self) -> list:
        driver: WebDriver = self.engine.native_driver

        image_list = []
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.XPATH, self.locator))
            )

            img_elements = driver.find_elements(By.XPATH, self.locator)

            for img in img_elements:
                src = img.get_attribute('src')
                if src:
                    image_list.append(src)
        except TimeoutException:
            pass

        return image_list


class GetDetailSelenium(BaseGetDetail):
    async def get_text_from_spans(self, rows: list, index: int) -> tuple[str, str] | None:
        row = rows[index]
        spans = row.find_elements(By.TAG_NAME, "span")

        if len(spans) >= 2:
            key = spans[0].get_attribute("textContent")
            value = spans[-1].get_attribute("textContent")
            if key and value:
                return key.strip(), value.strip()
        return None

    async def execute(self) -> dict[str, str]:
        driver: WebDriver = self.engine.native_driver

        details = {}
        try:
            rows = driver.find_elements(By.XPATH, self.locator)
            row_count = len(rows)
            for i in range(row_count):
                try:
                    span_texts = await self.get_text_from_spans(rows, i)
                    if span_texts:
                        key, value = span_texts
                        if key and value:
                            key_clean, val_clean = self.normalize_text(key, value)
                            exclusion = ExcludeField().details
                            if not self.is_in_excluded_field(text=key_clean, exclusion=exclusion):
                                details[key_clean] = val_clean.strip()
                except Exception as e:
                    print(f"Помилка в характеристиках (рядок {i}): {e}")
                    continue
        except Exception as e:
            print(f"Не вдалося знайти таблицю характеристик: {e}")
        return details
