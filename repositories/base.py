from typing import TypeVar, Generic, Any, Dict, Callable

from asgiref.sync import sync_to_async
from django.db.models import Model

from entities.base import BaseEntity
from utils.converters.model_to_entity import model_to_entity

_Model = TypeVar('_Model', bound=Model)
_Entity = TypeVar('_Entity', bound=BaseEntity)


class BaseRepository(Generic[_Model, _Entity]):
    model: type[_Model] = None
    entity: type[_Entity] = None
    map_to_entity: Callable = model_to_entity

    def __init__(
            self,
            model: type[_Model] = None,
            entity: type[_Entity] = None,
            map_to_entity: Callable = None,
    ) -> None:
        self.model = model or getattr(self, 'model', None)
        self.entity = entity or getattr(self, 'entity', None)
        self.map_to_entity = map_to_entity or getattr(type(self), 'map_to_entity', model_to_entity)

        assert self.model is not None, 'You must set "model" in constructor or class attribute'
        assert self.entity is not None, 'You must set "entity" in constructor or class attribute'


class ParserRepository(BaseRepository[_Model, _Entity]):
    def create(self, **fields: Dict[str, Any]) -> _Entity:
        obj = self.model.objects.create(**fields)
        return self.map_to_entity(obj=obj, entity_cls=self.entity)
