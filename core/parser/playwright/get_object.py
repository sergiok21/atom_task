from playwright.async_api import Page
from core.parser.meta.property import ExcludeField
from core.parser.meta.get_object import BaseGetImage, BaseGetDetail


class GetImagePlaywright(BaseGetImage):
    """Command to extract image source URLs using Playwright."""
    async def execute(self) -> list:
        """Waits for images to attach and retrieves all 'src' attributes."""
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
    """Command to extract product specifications using Playwright locators."""
    async def get_text_from_spans(self, rows, index) -> tuple[str, str] | None:
        """Extracts text from key and value spans within a specific row."""
        row = rows.nth(index)
        spans = row.locator("span")
        if await spans.count() >= 2:
            key = await spans.nth(0).text_content(timeout=1000)
            value = await spans.nth(-1).text_content(timeout=1000)
            if key and value:
                return key, value
        return None

    async def execute(self) -> dict[str, str]:
        """Iterates through rows to build a filtered dictionary of details."""
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
                print(f"Error in specifications (row {i}): {e}")
                continue
        return details