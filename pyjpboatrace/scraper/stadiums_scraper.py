import datetime
from logging import Logger, getLogger
from selenium import webdriver
from typing import Any, Dict


from .base import BaseScraper
from ..const import BOATRACEJP_BASE_URL
from ..parsers import parse_html_index


class StadiumsScraper(BaseScraper):
    """To get stadiums where races are/were held.
    """

    __url_format = f"{BOATRACEJP_BASE_URL}/index?hd={{date}}"

    def __init__(
        self,
        driver: webdriver.remote.webdriver.WebDriver,
        logger: Logger = getLogger(__name__),
    ):
        super().__init__(driver, parse_html_index, logger)

    @classmethod
    def make_url(cls, d: datetime.date) -> str:
        return cls.__url_format.format(date=d.strftime("%Y%m%d"))

    def get(self, d: datetime.date) -> Dict[str, Any]:
        return super().get(d)
