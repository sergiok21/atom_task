from abc import ABC, abstractmethod
from typing import Any


class BaseCommand(ABC):
    @abstractmethod
    def execute(self):
        pass


class BaseParser(ABC):
    @abstractmethod
    def parse(self) -> dict[str, Any]:
        pass
