import datetime
from logging import Logger, getLogger
from selenium import webdriver
from typing import Any, Dict


from .base import BaseScraper
from ..const import BOATRACEJP_BASE_URL
from ..parsers import parse_html_raceresult


class ResultScraper(BaseScraper):
    """To get race result
    """

    __url_format = f"{BOATRACEJP_BASE_URL}/raceresult?rno={{race}}&jcd={{stadium:02d}}&hd={{date}}"  # noqa

    def __init__(
        self,
        driver: webdriver.remote.webdriver.WebDriver,
        logger: Logger = getLogger(__name__),
    ):
        super().__init__(driver, parse_html_raceresult, logger)

    @classmethod
    def make_url(cls, d: datetime.date, stadium: int, race: int) -> str:
        return cls.__url_format.format(
            stadium=stadium,
            date=d.strftime("%Y%m%d"),
            race=race,
        )

    def get(self, d: datetime.date, stadium: int, race: int) -> Dict[str, Any]:
        return super().get(d, stadium, race)
