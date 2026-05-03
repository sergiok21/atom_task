from core.load_django import *
import asyncio

from core.parser.bs4.runner import BS4Parser
from core.parser.meta.property import Url
from core.parser.playwright.runner import PlaywrightParser
from core.parser.selenium.runner import SeleniumParser

if __name__ == '__main__':
    asyncio.run(PlaywrightParser(url=Url.base_url).parse())
    asyncio.run(SeleniumParser(url=Url.base_url).parse())
    asyncio.run(BS4Parser(url=Url.target_url).parse())
