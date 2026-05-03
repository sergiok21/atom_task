from core.load_django import *
import asyncio

from core.parser.property import Url
from core.parser.playwright.runner import PlaywrightParser


if __name__ == '__main__':
    asyncio.run(PlaywrightParser(url=Url.base_url).parse())
