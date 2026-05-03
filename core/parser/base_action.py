from abc import ABC, abstractmethod


class BaseSearchFieldAction(ABC):
    @abstractmethod
    async def fill_and_send(self, locator: str, text: str) -> None: ...


class BaseButtonAction(ABC):
    @abstractmethod
    async def click(self, locator) -> None: ...
