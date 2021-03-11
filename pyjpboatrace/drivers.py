import requests
import requests_cache
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from msedge.selenium_tools import Edge, EdgeOptions

from requests.exceptions import ConnectionError, InvalidSchema
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import InvalidArgumentException


def create_chrome_driver():
    # options
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--disable-web-security')
    options.add_argument('--lang=ja')
    options.add_argument('--blink-settings=imagesEnabled=false')
    # create driver
    driver = webdriver.Chrome(
        ChromeDriverManager().install(),
        options=options
    )
    return driver


def create_firefox_driver():
    # options
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    # create driver
    driver = webdriver.Firefox(
        executable_path=GeckoDriverManager().install(),
        options=options
    )
    return driver


def create_edge_driver():
    # options
    options = EdgeOptions()
    options.use_chromium = True
    options.add_argument("headless")
    options.add_argument("disable-gpu")
    # create driver
    driver = Edge(
        executable_path=EdgeChromiumDriverManager().install(),
        options=options
    )
    return driver


def create_httpget_driver():
    return HTTPGetDriver()


class HTTPGetDriver:
    """
    Wrapper class for requests.get as a webdriver of selenium,
    altough this class provides only get method and page_source property.
    """

    # TODO Need inheritance ?

    def __init__(self):
        self.__page_source = ''
        requests_cache.install_cache(cache_name='cache', backend="memory", expire_after=60 * 60 * 2)

    def get(self, url: str, use_cache: bool = False):
        """
        Loads a web page in the current browser session.
        """

        try:
            if use_cache == False:
                with requests_cache.disabled():
                    self.__page_source = requests.get(url).text
            else:
                self.__page_source = requests.get(url).text
                
        except ConnectionError:
            raise WebDriverException
        except InvalidSchema:
            raise InvalidArgumentException
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
