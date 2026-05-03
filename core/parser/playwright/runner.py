import asyncio

from playwright.async_api import async_playwright

from core.parser.base import Url
from core.parser.playwright.action import SearchFieldAction, ButtonAction
from core.parser.playwright.get_object import GetFullNamePlaywright, GetColorPlaywright, GetStoragePlaywright, \
    GetProducerPlaywright, GetDefaultPricePlaywright, GetSalePricePlaywright, GetExistPlaywright, GetImagePlaywright, \
    GetProductCodePlaywright, GetFeedbackPlaywright, GetDiagonalPlaywright, GetPixelPlaywright, GetDetailPlaywright
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
            await page.goto(self.url)

            await page.wait_for_load_state('domcontentloaded', timeout=4000)

            search_field_action, button_action = SearchFieldAction(page), ButtonAction(page)
            await search_field_action.fill_and_send()
            await button_action.click()

            await page.wait_for_load_state('domcontentloaded')

            get_field_pipeline = {
                "full_name": GetFullNamePlaywright(page),
                "color": GetColorPlaywright(page),
                "storage": GetStoragePlaywright(page),
                "producer": GetProducerPlaywright(page),
                "default_price": GetDefaultPricePlaywright(page),
                "sale_price": GetSalePricePlaywright(page),
                "exist": GetExistPlaywright(page),
                "image_list": GetImagePlaywright(page),
                "product_code": GetProductCodePlaywright(page),
                "feedback_count": GetFeedbackPlaywright(page),
                "diagonal": GetDiagonalPlaywright(page),
                "pixels": GetPixelPlaywright(page),
                "details": GetDetailPlaywright(page)
            }

            output_data = await execute_commands(pipeline=get_field_pipeline)

            iphone_entity = IPhoneEntity(**output_data)

            iphone_repo = IPhoneRepository()
            output = await sync_to_async_func(iphone_repo.create, **iphone_entity.__dict__)

            print(output)

            await browser.close()

            return output
