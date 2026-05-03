from typing import Any

import aiohttp
from bs4 import BeautifulSoup

from core.parser.meta.parser import BaseParser
from core.parser.meta.property import BS4Locator, Url
from core.parser.bs4.engine import BS4Engine
from core.parser.bs4.get_object import GetImageBS4, GetDetailBS4
from core.parser.meta.get_object import (
    GetFullName, GetColor, GetStorage, GetProducer,
    GetDefaultPrice, GetSalePrice, GetExist, GetProductCode,
    GetFeedback, GetDiagonal, GetPixel
)
from entities.iphone_entity import IPhoneEntity
from utils.process_manager import execute_commands


class BS4Parser(BaseParser):
    """Asynchronous parser implementation using BeautifulSoup and aiohttp.

    This parser fetches HTML content statically and processes it through
    a command-based pipeline to extract product data.
    """

    def __init__(self, url: str = Url.target_url):
        """Initializes the parser with a target URL.

        Args:
            url: The string URL of the product page to be parsed.
        """
        self.url = url

    async def fetch_html(self) -> str:
        """Performs an asynchronous HTTP GET request to retrieve page source.

        Returns:
            The raw HTML content as a string.

        Raises:
            aiohttp.ClientResponseError: If the HTTP request fails.
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(self.url) as response:
                response.raise_for_status()
                return await response.text()

    def create_pipeline(self, engine: BS4Engine) -> dict[str, Any]:
        """Assembles the command pipeline for data extraction.

        Args:
            engine: An instance of BS4Engine initialized with the page soup.

        Returns:
            A dictionary mapping field names to their respective
            command objects.
        """
        return {
            "full_name": GetFullName(engine, BS4Locator.full_name),
            "color": GetColor(engine, BS4Locator.color),
            "storage": GetStorage(engine, BS4Locator.storage),
            "producer": GetProducer(engine, BS4Locator.producer),
            "default_price": GetDefaultPrice(engine, BS4Locator.default_price),
            "sale_price": GetSalePrice(engine, BS4Locator.sale_price),
            "exist": GetExist(engine, BS4Locator.exist),
            "image_list": GetImageBS4(engine, BS4Locator.image_list),
            "product_code": GetProductCode(engine, BS4Locator.product_code),
            "feedback_count": GetFeedback(engine, BS4Locator.feedback_count),
            "diagonal": GetDiagonal(engine, BS4Locator.diagonal),
            "pixels": GetPixel(engine, BS4Locator.pixels),
            "details": GetDetailBS4(engine, BS4Locator.details),
        }

    async def parse(self) -> IPhoneEntity:
        """Executes the full parsing, validation, and storage lifecycle.

        1. Fetches HTML content.
        2. Initializes the BeautifulSoup engine.
        3. Executes the command pipeline to gather raw data.
        4. Validates data through the Entity layer.
        5. Persists data via the Repository layer.

        Returns:
            A validated IPhoneEntity instance containing the parsed data.
        """
        html_content = await self.fetch_html()
        soup = BeautifulSoup(html_content, 'lxml')
        engine = BS4Engine(soup)

        get_field_pipeline = self.create_pipeline(engine)
        output_data = await execute_commands(pipeline=get_field_pipeline)

        iphone_entity = IPhoneEntity(**output_data)
        output_entity = await self.save_data(data=iphone_entity.__dict__, entity_cls=IPhoneEntity)

        print(output_entity)

        return output_entity
