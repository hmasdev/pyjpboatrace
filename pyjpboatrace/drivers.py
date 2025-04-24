from typing import Callable

import requests
from requests import Response
from requests.exceptions import ConnectionError, InvalidSchema
from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException, WebDriverException
from selenium.webdriver.edge.options import Options as EdgeOptions


def create_chrome_driver() -> webdriver.Chrome:
    """Create an instance of chrome driver with headless mode

    Returns:
        webdriver.Chrome: chrome driver
    """
    # options
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--disable-web-security')
    options.add_argument('--lang=ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7')
    options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_argument(
        '--user-agent='
        '"Mozilla\\/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit\\/537.36 (KHTML, like Gecko) '
        'Chrome\\/89.0.4389.90 '
        '\\Safari/537.36"'
    )
    # create driver
    driver = webdriver.Chrome(options=options)
    return driver


def create_firefox_driver() -> webdriver.Firefox:
    """Create an instance of firefox driver with headless mode

    Returns:
        webdriver.Firefox: firefox driver
    """
    # options
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    # profile
    profile = webdriver.FirefoxProfile()
    profile.set_preference(
        'general.useragent.override',
        ''.join([
            '"Mozilla/5.0 (Windows NT 10.0; Win64; x64) ',
            'AppleWebKit/537.36 (KHTML, like Gecko) ',
            'Chrome/89.0.4389.90 ',
            'Safari/537.36"',
        ])
    )
    options.profile = profile
    # create driver
    driver = webdriver.Firefox(options=options)
    return driver


def create_edge_driver() -> webdriver.Edge:
    """Create an instance of edge driver

    Returns:
        webdriver.Edge: chrome driver

    WARNING:
        driver is activated without headless mode
    """
    # options
    options = EdgeOptions()
    options.add_argument("--headless=new")  # TODO set user agent
    options.add_argument("disable-gpu")
    # create driver
    driver = webdriver.Edge(options=options)
    return driver


class HTTPGetDriver:
    """
    Wrapper class for requests.get as a webdriver of selenium,
    altough this class provides only get method and page_source property.
    """

    # TODO Need inheriting selenium.webdriver.remote.webdriver.BaseWebDriver

    def __init__(
        self,
        http_get: Callable[[str, ], Response],
    ):
        self.__get = http_get
        self.__page_source = ''

    def get(self, url: str):
        """
        Loads a web page in the current browser session.
        """
        try:
            self.__page_source = self.__get(url).text
        except ConnectionError as e:
            raise WebDriverException from e
        except InvalidSchema as e:
            raise InvalidArgumentException from e
        return None

    @property
    def page_source(self):
        """
        Gets the source of the current page.
        :Usage:
            ::
                driver.page_source
        """
        return self.__page_source

    def close(self):
        pass


def create_httpget_driver(
    http_get: Callable[[str, ], Response] = requests.get,
) -> HTTPGetDriver:
    """Craete an instance of HTTPGetDriver

    Args:
        http_get (Callable[[str, ], Response], optional): HTTP get function.
            Defaults to requests.get.

    Returns:
        HTTPGetDriver: [description]
    """
    return HTTPGetDriver(http_get)
