from abc import ABCMeta, abstractmethod
from logging import Logger, getLogger
from typing import Any, Callable, Dict

from selenium import webdriver

_logger: Logger = getLogger(__name__)

class BaseScraper(metaclass=ABCMeta):
    """Base class for scraper.
    """

    def __init__(
        self,
        driver: webdriver.remote.webdriver.WebDriver,
        parser: Callable[[str, ], Dict[str, Any]],
        logger: Logger = _logger,
    ):
        self._driver = driver
        self._parser = parser
        self._logger = logger

    @classmethod
    @abstractmethod
    def make_url(cls, *args, **kwargs) -> str:
        raise NotImplementedError()

    def get(self, *args, **kwargs) -> Dict[str, Any]:
        url = self.make_url(*args, **kwargs)
        self._logger.info(f"URL created: {url}")
        self._driver.get(url)
        html = self._driver.page_source
        return self._parser(html)
