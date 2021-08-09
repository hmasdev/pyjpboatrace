import datetime
from logging import Logger, getLogger
from selenium import webdriver
from typing import Any, Dict


from .base import BaseScraper
from ..const import BOATRACEJP_BASE_URL
from ._parser import parse_html_raceindex
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
        """Make target URL.

        Args:
            d (datetime.date): race date
            stadium (int): stadium no.

        Returns:
            str: URL
        """
        return cls.__url_format.format(
            stadium=stadium,
            date=d.strftime("%Y%m%d")
        )

    def get(self, d: datetime.date, stadium: int) -> Dict[str, Any]:
        """Get 12 races held in the given stadium on the given date.

        Args:
            d (datetime.date): race date
            stadium (int): stadium no.

        Raises:
            ValueError: Occurred when invalid date given.
            ValueError: Occurred when invalid stadium no. given.

        Returns:
            Dict[str, Any]: scraped data
        """
        validate_date(d)
        validate_stadium(stadium)
        dic = super().get(d, stadium)
        dic.update(
            date=d.strftime("%Y-%m-%d"),
            stadium=stadium,
        )
        return dic
