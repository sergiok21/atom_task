from abc import ABC, abstractmethod
from typing import Any, Type, TypeVar

from core.parser.meta.engine import BaseScraperEngine
from entities.base import BaseEntity
from entities.iphone_entity import IPhoneEntity
from repositories.base import BaseRepository
from repositories.iphone_repo import IPhoneRepository
from utils.process_manager import sync_to_async_func

_Entity = TypeVar('_Entity', bound=BaseEntity)


class BaseParser(ABC):
    """Abstract base class for the high-level parsing logic."""

    @abstractmethod
    async def parse(self) -> _Entity:
        """Orchestrates the full scraping and saving process."""
        pass

    @abstractmethod
    def create_pipeline(self, engine: BaseScraperEngine) -> dict[str, Any]:
        """Defines the mapping of fields to extraction commands."""
        pass

    async def save_data(
            self,
            data: dict[str, Any],
            entity_cls: Type[_Entity] = IPhoneEntity,
            repository: BaseRepository = IPhoneRepository()
    ) -> _Entity:
        """Validates raw data into an entity and persists it via repository.

        Args:
            data: Raw dictionary of parsed data.
            entity_cls: The entity class for validation.
            repository: The repository instance for database operations.
        """
        entity_obj = entity_cls(**data)
        return await sync_to_async_func(repository.create, **entity_obj.__dict__)