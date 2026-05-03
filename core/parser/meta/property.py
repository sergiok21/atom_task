from dataclasses import dataclass, field


@dataclass(frozen=True)
class XPathLocator:
    """Container for XPath-based element locators."""
    search_field: str = "//div[@class='header-bottom']//input[@class='quick-search-input']"
    element_from_grid = "//div[contains(@class, 'product-wrapper')]//div[@class='br-pp-img br-pp-img-grid']/a"

    full_name: str = "//h1[@class='desktop-only-title']"
    color: str = "//a[contains(@title, 'Колір')]"
    storage: str = "//span/a[contains(@title, 'Вбудована пам')]"
    producer: str = "//div[contains(@class, 'br-pr-chr-item')]//span[contains(text(), 'Виробник')]/following-sibling::span"
    default_price: str = "//div[@class='price-wrapper']/span"
    sale_price: str = "//div[@class='price-wrapper']/span[@class='red-price']"
    exist: str = "//div[@class='br-pr-no-del']/strong"
    image_list: str = "//a[@class='product-modal-button']/img[@class='br-main-img']"
    product_code: str = "(//div[@id='product_code'])[1]/span[@class='br-pr-code-val']"
    feedback_count: str = "//a[@href='#reviews-list' and @class='scroll-to-element']/span"
    diagonal: str = "//span/a[contains(@title, 'Діагональ')]"
    pixels: str = "//span/a[contains(@title, 'Роздільна здатність екрану')]"
    details: str = "//div[contains(@class, 'br-pr-chr-item')]/div/div"


@dataclass(frozen=True)
class BS4Locator:
    """Container for CSS selector-based element locators."""
    full_name: str = "h1.desktop-only-title"
    color: str = "a[title*='Колір']"
    storage: str = "a[title*='Вбудована пам']"
    producer: str = "div.br-pr-chr-item span:-soup-contains('Виробник') + span"
    default_price: str = "div.price-wrapper span"
    sale_price: str = "div.price-wrapper span.red-price"
    exist: str = "div.br-pr-no-del strong"
    image_list: str = "a.product-modal-button img.br-main-img"
    product_code: str = "div#product_code span.br-pr-code-val"
    feedback_count: str = "a.scroll-to-element[href='#reviews-list'] span"
    diagonal: str = "a[title*='Діагональ']"
    pixels: str = "a[title*='Роздільна здатність']"
    details: str = "div.br-pr-chr-item > div > div"


@dataclass(frozen=True)
class Url:
    """Global URL configuration."""
    base_url: str = 'https://brain.com.ua/ukr/'
    target_url: str = f'{base_url}Mobilniy_telefon_Apple_iPhone_16_Pro_Max_256GB_Black_Titanium-p1145443.html'


@dataclass(frozen=True)
class ExcludeField:
    details: list = field(default_factory=lambda: ['Примітка'])


@dataclass(frozen=True)
class TextField:
    search_text: str = 'Apple iPhone 15 128GB Black'
