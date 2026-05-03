import re
from abc import abstractmethod, ABC

from core.parser.base import BaseCommand
from core.parser.engine import BaseScraperEngine
from utils.text_processor import TextProcessor


class BaseGetObject(BaseCommand, TextProcessor):
    def __init__(self, engine: BaseScraperEngine, locator: str):
        self.engine = engine
        self.locator = locator

    async def execute(self) -> int | str | float | list | dict | None:
        return await self.engine.get_text(self.locator)


class BaseGetImage(BaseGetObject):
    @abstractmethod
    async def execute(self) -> list:
        pass


class BaseGetDetail(BaseGetObject, ABC):
    def normalize_text(self, key: str, value: str) -> tuple[str, str]:
        key_clean = re.sub(r'\s+', ' ', str(key)).replace(':', '').strip()
        val_clean = re.sub(r'\s+', ' ', str(value)).strip()
        return key_clean, val_clean

    @abstractmethod
    async def get_text_from_spans(self, rows, index) -> tuple[str, str] | None:
        pass

    @abstractmethod
    async def execute(self) -> dict[str, str]:
        pass


class GetDefaultPrice(BaseGetObject):
    async def execute(self) -> int | float:
        default_price = await self.engine.get_text(self.locator)
        return self.extract_digits(default_price)


class GetSalePrice(BaseGetObject):
    async def execute(self) -> int | float:
        sale_price = await self.engine.get_text(self.locator)
        return self.extract_digits(sale_price)


class GetExist(BaseGetObject):
    async def execute(self) -> bool:
        return False if await self.engine.get_text(self.locator) else True


class GetFeedback(BaseGetObject):
    async def execute(self) -> int:
        feedback = await self.engine.get_text(self.locator)
        return self.extract_digits(feedback)


class GetDiagonal(BaseGetObject):
    def transform_to_float(self, diag_str: str | None) -> float:
        return float(diag_str.replace(',', '.').replace('"', '')) if diag_str else 0.0

    async def execute(self) -> float:
        diag_str = await self.engine.get_text(self.locator)
        return self.transform_to_float(diag_str)


class GetFullName(BaseGetObject): ...


class GetColor(BaseGetObject): ...


class GetStorage(BaseGetObject): ...


class GetProducer(BaseGetObject): ...


class GetProductCode(BaseGetObject): ...


class GetPixel(BaseGetObject): ...
