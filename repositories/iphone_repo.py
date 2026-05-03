from entities.iphone_entity import IPhoneEntity
from parser_app.models import IPhone
from repositories.base import ParserRepository


class IPhoneRepository(ParserRepository[IPhone, IPhoneEntity]):
    model = IPhone
    entity = IPhoneEntity
