from playwright.async_api import async_playwright

from core.parser.property import XPathLocator, Url
from core.parser.engine import PlaywrightEngine
from core.parser.playwright.action import SearchFieldActionPlaywright, ButtonActionPlaywright
from core.parser.playwright.get_object import GetImagePlaywright, GetDetailPlaywright
from core.parser.get_object import GetFullName, GetColor, GetStorage, \
    GetProducer, GetDefaultPrice, GetSalePrice, GetExist, GetProductCode, GetFeedback, GetDiagonal, GetPixel
from entities.iphone_entity import IPhoneEntity
from repositories.iphone_repo import IPhoneRepository
from utils.process_manager import execute_commands, sync_to_async_func


class PlaywrightParser:
    def __init__(self, url: str = Url.base_url):
        self.url = url

    async def parse(self) -> dict:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            page = await browser.new_page()

            engine = PlaywrightEngine(page)

            await page.goto(self.url)

            await page.wait_for_load_state('domcontentloaded', timeout=4000)

            search_field_action, button_action = SearchFieldActionPlaywright(page), ButtonActionPlaywright(page)
            await search_field_action.fill_and_send()
            await button_action.click()

            await page.wait_for_load_state('domcontentloaded')

            get_field_pipeline = {
                "full_name": GetFullName(engine, XPathLocator.full_name),
                "color": GetColor(engine, XPathLocator.color),
                "storage": GetStorage(engine, XPathLocator.storage),
                "producer": GetProducer(engine, XPathLocator.producer),
                "default_price": GetDefaultPrice(engine, XPathLocator.default_price),
                "sale_price": GetSalePrice(engine, XPathLocator.sale_price),
                "exist": GetExist(engine, XPathLocator.exist),
                "image_list": GetImagePlaywright(engine, XPathLocator.image_list),
                "product_code": GetProductCode(engine, XPathLocator.product_code),
                "feedback_count": GetFeedback(engine, XPathLocator.feedback_count),
                "diagonal": GetDiagonal(engine, XPathLocator.diagonal),
                "pixels": GetPixel(engine, XPathLocator.pixels),
                "details": GetDetailPlaywright(engine, XPathLocator.details),
            }

            output_data = await execute_commands(pipeline=get_field_pipeline)

            iphone_entity = IPhoneEntity(**output_data)

            iphone_repo = IPhoneRepository()
            output = await sync_to_async_func(iphone_repo.create, **iphone_entity.__dict__)

            print(output)

            await browser.close()

            return output
