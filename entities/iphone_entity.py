from dataclasses import dataclass
from typing import Any

from entities.base import BaseEntity


@dataclass
class IPhoneEntity(BaseEntity):
    full_name: str
    color: str
    storage: str
    producer: str
    default_price: float | None
    sale_price: float | None
    exist: bool
    image_list: list[str]
    product_code: str
    feedback_count: int
    diagonal: float
    pixels: str
    details: dict[str, Any]


@dataclass
class IPhoneEntityOut(IPhoneEntity):
    pk: int
