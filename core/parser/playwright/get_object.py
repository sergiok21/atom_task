from playwright.async_api import Page

from core.parser.property import ExcludeField
from core.parser.get_object import BaseGetImage, BaseGetDetail


class GetImagePlaywright(BaseGetImage):
    async def execute(self) -> list:
        page: Page = self.engine.native_driver

        image_list = []
        await page.wait_for_selector(self.locator, state="attached", timeout=5000)
        img_locators = await page.locator(self.locator).all()
        for img in img_locators:
            src = await img.get_attribute('src')
            if src:
                image_list.append(src)
        return image_list


class GetDetailPlaywright(BaseGetDetail):
    async def get_text_from_spans(self, rows, index) -> tuple[str, str] | None:
        row = rows.nth(index)
        spans = row.locator("span")

        if await spans.count() >= 2:
            key = await spans.nth(0).text_content(timeout=1000)
            value = await spans.nth(-1).text_content(timeout=1000)

            if key and value:
                return key, value
        return None

    async def execute(self) -> dict[str, str]:
        page: Page = self.engine.native_driver

        details = {}
        rows = page.locator(self.locator)
        row_count = await rows.count()

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
        return details
