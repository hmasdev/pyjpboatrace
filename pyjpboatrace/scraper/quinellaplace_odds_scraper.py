import datetime
from logging import Logger, getLogger
from selenium import webdriver
from typing import Any, Dict


from .base import BaseScraper
from ..const import BOATRACEJP_BASE_URL
from ..parsers import parse_html_oddsk
from ..validator import validate_date, validate_stadium, validate_race


class QuinellaplaceOddsScraper(BaseScraper):
    """To get quinellaplace odds
    """

    __url_format = f"{BOATRACEJP_BASE_URL}/oddsk?rno={{race}}&jcd={{stadium:02d}}&hd={{date}}"  # noqa

    def __init__(
        self,
        driver: webdriver.remote.webdriver.WebDriver,
        logger: Logger = getLogger(__name__),
    ):
        super().__init__(driver, parse_html_oddsk, logger)

    @classmethod
    def make_url(cls, d: datetime.date, stadium: int, race: int) -> str:
        return cls.__url_format.format(
            stadium=stadium,
            date=d.strftime("%Y%m%d"),
            race=race,
        )

    def get(self, d: datetime.date, stadium: int, race: int) -> Dict[str, Any]:
        validate_date(d)
        validate_stadium(stadium)
        validate_race(race)
        return super().get(d, stadium, race)
