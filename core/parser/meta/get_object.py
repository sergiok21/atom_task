import re
from abc import abstractmethod, ABC

from core.parser.meta.command import BaseCommand
from core.parser.meta.engine import BaseScraperEngine
from utils.text_processor import TextProcessor


class BaseGetObject(BaseCommand, TextProcessor):
    """Base class for commands that retrieve data objects via a scraper engine."""

    def __init__(self, engine: BaseScraperEngine, locator: str):
        """Initializes the command with an engine and a locator.

        Args:
            engine: The scraper engine to use.
            locator: The element locator string.
        """
        self.engine = engine
        self.locator = locator

    async def execute(self) -> int | str | float | list | dict | None:
        """Retrieves raw text content via the engine."""
        return await self.engine.get_text(self.locator)


class BaseGetImage(BaseGetObject):
    """Abstract class for commands specifically retrieving image data."""

    @abstractmethod
    async def execute(self) -> list:
        """Must be implemented to return a list of image URLs."""
        pass


class BaseGetDetail(BaseGetObject, ABC):
    """Abstract class for extracting complex product specifications."""

    def normalize_text(self, key: str, value: str) -> tuple[str, str]:
        """Cleans and formats specification keys and values."""
        key_clean = re.sub(r'\s+', ' ', str(key)).replace(':', '').strip()
        val_clean = re.sub(r'\s+', ' ', str(value)).strip()
        return key_clean, val_clean

    @abstractmethod
    async def get_text_from_spans(self, rows, index) -> tuple[str, str] | None:
        """Extracts pair data from row elements."""
        pass


class GetDefaultPrice(BaseGetObject):
    """Command to retrieve and parse the standard product price."""

    async def execute(self) -> int | float:
        """Extracts numeric digits from the price text."""
        default_price = await self.engine.get_text(self.locator)
        return self.extract_digits(default_price)


class GetSalePrice(BaseGetObject):
    """Command to retrieve and parse the promotional product price."""

    async def execute(self) -> int | float:
        """Extracts numeric digits from the sale price text."""
        sale_price = await self.engine.get_text(self.locator)
        return self.extract_digits(sale_price)


class GetExist(BaseGetObject):
    """Command to determine product availability."""

    async def execute(self) -> bool:
        """Checks if the 'out of stock' indicator is present."""
        return False if await self.engine.get_text(self.locator) else True


class GetFeedback(BaseGetObject):
    """Command to retrieve the total count of product reviews."""

    async def execute(self) -> int:
        """Extracts digits representing the review count."""
        feedback = await self.engine.get_text(self.locator)
        return self.extract_digits(feedback)


class GetDiagonal(BaseGetObject):
    """Command to retrieve and convert screen diagonal size."""

    def transform_to_float(self, diag_str: str | None) -> float:
        """Converts string measurements (e.g., 6.1") to float."""
        return float(diag_str.replace(',', '.').replace('"', '')) if diag_str else 0.0

    async def execute(self) -> float:
        """Retrieves diagonal text and transforms it."""
        diag_str = await self.engine.get_text(self.locator)
        return self.transform_to_float(diag_str)


class GetFullName(BaseGetObject): ...


class GetColor(BaseGetObject): ...


class GetStorage(BaseGetObject): ...


class GetProducer(BaseGetObject): ...


class GetProductCode(BaseGetObject): ...


class GetPixel(BaseGetObject): ...
