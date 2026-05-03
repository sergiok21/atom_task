from bs4 import BeautifulSoup, Tag

from core.parser.meta.property import ExcludeField
from core.parser.meta.get_object import BaseGetImage, BaseGetDetail


class GetImageBS4(BaseGetImage):
    """BeautifulSoup implementation for extracting image URLs.

    This class retrieves all 'src' attributes from image elements found
    using the specified CSS selector.
    """

    async def execute(self) -> list:
        """Extracts a list of image source URLs from the parsed HTML.

        Returns:
            A list of strings containing image URLs. Returns an empty list
            if no images are found or if an error occurs.
        """
        soup: BeautifulSoup = self.engine.native_driver
        image_list = []

        try:
            img_elements = soup.select(self.locator)
            for img in img_elements:
                src = img.get('src')
                if src:
                    image_list.append(src)
        except Exception as e:
            print(f"Помилка збору зображень: {e}")

        return image_list


class GetDetailBS4(BaseGetDetail):
    """BeautifulSoup implementation for extracting product specifications.

    This class parses product detail rows, typically formatted as key-value
    pairs within span elements, and cleans them based on exclusion rules.
    """

    async def get_text_from_spans(self, rows: list[Tag], index: int) -> tuple[str, str] | None:
        """Extracts key-value pairs from span elements within a specific row.

        Args:
            rows: A list of BeautifulSoup Tag objects representing detail rows.
            index: The current row index to process.

        Returns:
            A tuple of (key, value) strings if found and valid; otherwise None.
        """
        row = rows[index]
        spans = row.find_all("span")

        if len(spans) >= 2:
            key = spans[0].get_text(strip=True)
            value = spans[-1].get_text(strip=True)
            if key and value:
                return key, value
        return None

    async def execute(self) -> dict[str, str]:
        """Processes all rows to build a dictionary of product specifications.

        Iterates through HTML elements, cleans the text, and filters out
        fields defined in the ExcludeField configuration.

        Returns:
            A dictionary where keys are specification names and values are
            their corresponding details.
        """
        soup: BeautifulSoup = self.engine.native_driver
        details = {}

        try:
            rows = soup.select(self.locator)
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
                                details[key_clean] = val_clean
                except Exception as e:
                    print(f"Помилка в характеристиках (рядок {i}): {e}")
                    continue
        except Exception as e:
            print(f"Не вдалося знайти таблицю характеристик: {e}")

        return details
