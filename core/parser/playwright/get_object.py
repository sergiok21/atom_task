import re
from typing import Any

from playwright.async_api import Page

from core.parser.base import BaseCommand, XPathLocator, ExcludeField


class BaseGetObjectPlaywright(BaseCommand):
    def __init__(self, page: "Page", locator: str):
        self.page = page
        self.locator = locator

    async def get_text_from_xpath(self, page: "Page", xpath: str) -> str | None:
        try:
            element = page.locator(xpath).first
            return await element.inner_text(timeout=2000)
        except Exception as e:
            return None

    def extract_digits(self, text: str | None) -> int:
        if not text: return 0
        digits = re.sub(r'[^\d]', '', text)
        return int(digits) if digits else 0

    def is_in_excluded_field(self, text: str, exclusion: list[Any]) -> bool:
        return text in exclusion

    async def execute(self) -> int | str | float | list | dict | None:
        return await self.get_text_from_xpath(self.page, self.locator)


class GetFullNamePlaywright(BaseGetObjectPlaywright):
    def __init__(self, page: "Page", locator: str = XPathLocator.full_name):
        super().__init__(page, locator)


class GetColorPlaywright(BaseGetObjectPlaywright):
    def __init__(self, page: "Page", locator: str = XPathLocator.color):
        super().__init__(page, locator)


class GetStoragePlaywright(BaseGetObjectPlaywright):
    def __init__(self, page: "Page", locator: str = XPathLocator.storage):
        super().__init__(page, locator)


class GetProducerPlaywright(BaseGetObjectPlaywright):
    def __init__(self, page: "Page", locator: str = XPathLocator.producer):
        super().__init__(page, locator)


class GetDefaultPricePlaywright(BaseGetObjectPlaywright):
    def __init__(self, page: "Page", locator: str = XPathLocator.default_price):
        super().__init__(page, locator)

    async def execute(self) -> int | float:
        default_price = await self.get_text_from_xpath(self.page, self.locator)
        return self.extract_digits(default_price)


class GetSalePricePlaywright(BaseGetObjectPlaywright):
    def __init__(self, page: "Page", locator: str = XPathLocator.sale_price):
        super().__init__(page, locator)

    async def execute(self) -> int | float:
        sale_price = await self.get_text_from_xpath(self.page, self.locator)
        return self.extract_digits(sale_price)


class GetExistPlaywright(BaseGetObjectPlaywright):
    def __init__(self, page: "Page", locator: str = XPathLocator.exist):
        super().__init__(page, locator)

    async def execute(self) -> bool:
        return False if await self.get_text_from_xpath(self.page, self.locator) else True


class GetImagePlaywright(BaseGetObjectPlaywright):
    def __init__(self, page: "Page", locator: str = XPathLocator.image_list):
        super().__init__(page, locator)

    async def execute(self) -> list:
        image_list = []
        await self.page.wait_for_selector(self.locator, state="attached", timeout=5000)
        img_locators = await self.page.locator(self.locator).all()
        for img in img_locators:
            src = await img.get_attribute('src')
            if src:
                image_list.append(src)
        return image_list


class GetProductCodePlaywright(BaseGetObjectPlaywright):
    def __init__(self, page: "Page", locator: str = XPathLocator.product_code):
        super().__init__(page, locator)


class GetFeedbackPlaywright(BaseGetObjectPlaywright):
    def __init__(self, page: "Page", locator: str = XPathLocator.feedback_count):
        super().__init__(page, locator)

    async def execute(self) -> int:
        feedback = await self.get_text_from_xpath(self.page, self.locator)
        return self.extract_digits(feedback)


class GetDiagonalPlaywright(BaseGetObjectPlaywright):
    def __init__(self, page: "Page", locator: str = XPathLocator.diagonal):
        super().__init__(page, locator)

    async def execute(self) -> float:
        diag_str = await self.get_text_from_xpath(self.page, self.locator)
        return float(diag_str.replace(',', '.').replace('"', '')) if diag_str else 0.0


class GetPixelPlaywright(BaseGetObjectPlaywright):
    def __init__(self, page: "Page", locator: str = XPathLocator.pixels):
        super().__init__(page, locator)


class GetDetailPlaywright(BaseGetObjectPlaywright):
    def __init__(self, page: "Page", locator: str = XPathLocator.details):
        super().__init__(page, locator)

    def _normalize_text(self, key: str, value: str) -> tuple[str, str]:
        key_clean = re.sub(r'\s+', ' ', str(key)).replace(':', '').strip()
        val_clean = re.sub(r'\s+', ' ', str(value)).strip()
        return key_clean, val_clean

    async def _get_text_from_spans(self, rows, index) -> tuple[str, str] | None:
        row = rows.nth(index)
        spans = row.locator("span")

        if await spans.count() >= 2:
            key = await spans.nth(0).text_content(timeout=1000)
            value = await spans.nth(-1).text_content(timeout=1000)

            if key and value:
                return key, value
        return None

    async def execute(self) -> dict[str, str]:
        details = {}
        rows = self.page.locator(self.locator)
        row_count = await rows.count()

        for i in range(row_count):
            try:
                span_texts = await self._get_text_from_spans(rows, i)
                if span_texts:
                    key, value = span_texts
                    if key and value:
                        key_clean, val_clean = self._normalize_text(key, value)
                        exclusion = ExcludeField().details
                        if not self.is_in_excluded_field(text=key_clean, exclusion=exclusion):
                            details[key_clean] = val_clean.strip()
            except Exception as e:
                print(f"Помилка в характеристиках (рядок {i}): {e}")
                continue
        return details
