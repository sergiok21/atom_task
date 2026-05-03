from typing import Any

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from core.parser.meta.parser import BaseParser
from core.parser.meta.property import XPathLocator, Url
from core.parser.selenium.engine import SeleniumEngine
from core.parser.selenium.action import SearchFieldActionSelenium, ButtonActionSelenium
from core.parser.selenium.get_object import GetImageSelenium, GetDetailSelenium
from core.parser.meta.get_object import (
    GetFullName, GetColor, GetStorage, GetProducer,
    GetDefaultPrice, GetSalePrice, GetExist, GetProductCode,
    GetFeedback, GetDiagonal, GetPixel
)
from entities.iphone_entity import IPhoneEntity
from utils.process_manager import execute_commands


class SeleniumParser(BaseParser):
    def __init__(self, url: str = Url.base_url):
        self.url = url

    def create_pipeline(self, engine: SeleniumEngine) -> dict[str, Any]:
        return {
            "full_name": GetFullName(engine, XPathLocator.full_name),
            "color": GetColor(engine, XPathLocator.color),
            "storage": GetStorage(engine, XPathLocator.storage),
            "producer": GetProducer(engine, XPathLocator.producer),
            "default_price": GetDefaultPrice(engine, XPathLocator.default_price),
            "sale_price": GetSalePrice(engine, XPathLocator.sale_price),
            "exist": GetExist(engine, XPathLocator.exist),
            "image_list": GetImageSelenium(engine, XPathLocator.image_list),
            "product_code": GetProductCode(engine, XPathLocator.product_code),
            "feedback_count": GetFeedback(engine, XPathLocator.feedback_count),
            "diagonal": GetDiagonal(engine, XPathLocator.diagonal),
            "pixels": GetPixel(engine, XPathLocator.pixels),
            "details": GetDetailSelenium(engine, XPathLocator.details),
        }

    async def parse(self) -> IPhoneEntity:
        chrome_options = Options()
        # chrome_options.add_argument("--headless")

        driver = webdriver.Chrome(options=chrome_options)

        try:
            engine = SeleniumEngine(driver)

            driver.get(self.url)

            search_field_action = SearchFieldActionSelenium(driver)
            button_action = ButtonActionSelenium(driver)

            await search_field_action.fill_and_send()
            await button_action.click()

            get_field_pipeline = self.create_pipeline(engine)
            output_data = await execute_commands(pipeline=get_field_pipeline)

            iphone_entity = IPhoneEntity(**output_data)
            output_entity = await self.save_data(data=iphone_entity.__dict__, entity_cls=IPhoneEntity)

            print(output_entity)

            return output_entity

        finally:
            driver.quit()
