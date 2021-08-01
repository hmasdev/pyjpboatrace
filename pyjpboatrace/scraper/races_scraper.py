import datetime
from logging import Logger, getLogger
from selenium import webdriver
from typing import Any, Dict


from .base import BaseScraper
from ..const import BOATRACEJP_BASE_URL
from ..parsers import parse_html_raceindex
from ..validator import validate_date, validate_stadium


class RacesScraper(BaseScraper):
    """To get 12 races held in a stadium
    """

    __url_format = f"{BOATRACEJP_BASE_URL}/raceindex?jcd={{stadium:02d}}&hd={{date}}"  # noqa

    def __init__(
        self,
        driver: webdriver.remote.webdriver.WebDriver,
        logger: Logger = getLogger(__name__),
    ):
        super().__init__(driver, parse_html_raceindex, logger)

    @classmethod
    def make_url(cls, d: datetime.date, stadium: int) -> str:
        return cls.__url_format.format(
            stadium=stadium,
            date=d.strftime("%Y%m%d")
        )

    def get(self, d: datetime.date, stadium: int) -> Dict[str, Any]:
        validate_date(d)
        validate_stadium(stadium)
        return super().get(d, stadium)
