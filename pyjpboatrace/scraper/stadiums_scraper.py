import datetime
from logging import Logger, getLogger
from selenium import webdriver
from typing import Any, Dict


from .base import BaseScraper
from ..const import BOATRACEJP_BASE_URL
from ._parser import parse_html_index
from ..validator import validate_date


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
        """Make target URL.

        Args:
            d (datetime.date): race date

        Returns:
            str: URL
        """
        return cls.__url_format.format(date=d.strftime("%Y%m%d"))

    def get(self, d: datetime.date) -> Dict[str, Any]:
        """Get stadiums where races are held on the given day.

        Args:
            d (datetime.date): race date

        Raises:
            ValueError: Occurred when invalid date given.

        Returns:
            Dict[str, Any]: scraped data
        """
        validate_date(d)
        return super().get(d)
