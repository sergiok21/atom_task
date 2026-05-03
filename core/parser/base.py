from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


class BaseCommand(ABC):
    @abstractmethod
    def execute(self):
        pass


@dataclass(frozen=True)
class XPathLocator:
    search_field: str = "//div[@class='header-bottom']//input[@class='quick-search-input']"
    element_from_grid = "//div[contains(@class, 'product-wrapper')]//div[@class='br-pp-img br-pp-img-grid']/a"

    full_name: str = "//h1[@class='desktop-only-title']"
    color: str = "//a[contains(@title, 'Колір')]"
    storage: str = "//span/a[contains(@title, 'Вбудована пам')]"
    producer: str = "//div[@class='br-pr-chr-item']/div/div[contains(span, 'Виробник')]/span[2]"
    default_price: str = "//div[@class='price-wrapper']/span"
    sale_price: str = "//div[@class='price-wrapper']/span[@class='red-price']"
    exist: str = "//div[@class='br-pr-no-del']/strong"
    image_list: str = "//a[@class='product-modal-button']/img[@class='br-main-img']"
    product_code: str = "(//div[@id='product_code'])[1]/span[@class='br-pr-code-val']"
    feedback_count: str = "//a[@href='#reviews-list' and @class='scroll-to-element']/span"
    diagonal: str = "//span/a[contains(@title, 'Діагональ')]"
    pixels: str = "//span/a[contains(@title, 'Роздільна здатність екрану')]"
    details: str = "//div[@class='br-pr-chr-item']/div/div"


@dataclass(frozen=True)
class BS4Locator:
    full_name: str = "h1.desktop-only-title"
    color: str = "a[title*='Колір'], a[title*='Цвет']"
    storage: str = "//span/a[contains(@title, 'Вбудована пам\'ять')]"
    diagonal: str = "a[title*='Діагональ'], a[title*='Диагональ']"
    pixels: str = "a[title*='Роздільна здатність'], a[title*='Разрешение']"
    default_price: str = "div.price-wrapper span"
    sale_price: str = "div.br-pr-no-del strong"
    image_list: str = "div.slick-slide:not(.item) img, div.slick-active:not(.item) img"
    product_code: str = "div#product_code span.br-pr-code-val"
    feedback_count: str = "a.scroll-to-element[href='#reviews-list'] span"
    details_row: str = "div.br-pr-chr-item"
    details_key: str = "span:nth-of-type(1)"
    details_value: str = "span:nth-of-type(2)"


@dataclass(frozen=True)
class Url:
    base_url: str = 'https://brain.com.ua/ukr/'
    target_url: str = f'{base_url}/Mobilniy_telefon_Apple_iPhone_16_Pro_Max_256GB_Black_Titanium-p1145443.html'


@dataclass(frozen=True)
class ExcludeField:
    details: list = field(default_factory=lambda: ['Примітка'])


class TextField:
    search_text: str = 'Apple iPhone 15 128GB Black'


class BaseParser(ABC):
    @abstractmethod
    def parse(self) -> dict[str, Any]:
        pass
