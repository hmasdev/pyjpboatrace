import datetime
from logging import getLogger
import sys

from bs4 import BeautifulSoup
from selenium import webdriver

from . import parsers
from .exceptions import NoDataException
from .const import BASE_URL, NUM_RACES, NUM_STADIUMS
from pyjpboatrace.drivers import create_chrome_driver


class PyJPBoatrace(object):

    def __init__(
        self,
        driver: webdriver.remote.webdriver.WebDriver = create_chrome_driver(),
        base_url: str = BASE_URL,
        logger=getLogger(__name__),
    ):
        self.__driver = driver
        self.__base_url = base_url
        self.__logger = logger

    def __baseget(self, url: str, parser) -> dict:

        self.__logger.debug(f'Start requesting {url}')
        self.__driver.get(url)
        html = self.__driver.page_source
        self.__logger.debug('Completed request')

        self.__logger.debug('Start validate html')
        try:
            self.__validate_contents(html)
        except NoDataException:
            # No data found
            self.__logger.warning('No data in html')
            return {}
        self.__logger.debug('Completed validation')

        self.__logger.debug('Start to parse html')
        dic = parser(html)
        self.__logger.debug('Completed to parse')

        return dic

    def __validate_args(
        self,
        d: datetime.date = None,
        stadium: int = None,
        race:  int = None
    ):

        if (d is not None) and (d > datetime.datetime.today().date()):
            raise ValueError(f'Date d must be before today. {d} is given.')
        if (stadium is not None) and (stadium < 1 or NUM_STADIUMS < stadium):
            raise ValueError(
                f'Stadium must be between 1 and {NUM_STADIUMS}. '
                f'{stadium} is given.'
            )
        if (race is not None) and (race < 1 or NUM_RACES < race):
            raise ValueError(
                f'Race must be between 1 and {NUM_RACES}. {race} is given.'
            )

    def __validate_contents(self, html: str):
        # preparation
        soup = BeautifulSoup(html, 'html.parser')

        # whether the dataset has not been displayed
        texts = map(
            lambda e: e.text,
            soup.select('h3.title12_title')
        )
        if '※ データはありません。' in texts:
            raise NoDataException()

        # whether the dataset is not found
        texts = map(
            lambda e: e.text,
            soup.select('span.heading1_mainLabel')
        )
        if 'データがありません。' in texts:
            raise NoDataException()

    def get_stadiums(self, d: datetime.date) -> dict:

        self.__logger.debug(f'{sys._getframe().f_code.co_name} called')
        # validation
        self.__validate_args(d)
        # format
        d = d.strftime('%Y%m%d')
        # get data and return the parsed object
        return self.__baseget(
            f'{self.__base_url}/index?hd={d}',
            parsers.parse_html_index
        )

    def get_12races(self, d: datetime.date, stadium: int) -> dict:

        self.__logger.debug(f'{sys._getframe().f_code.co_name} called')
        # validation
        self.__validate_args(d, stadium)
        # format
        d = d.strftime('%Y%m%d')
        stdm = str(stadium).zfill(2)
        # get data and return the parsed object
        return self.__baseget(
            f"{self.__base_url}/raceindex?jcd={stdm}&hd={d}",
            parsers.parse_html_raceindex
        )

    def get_race_info(self, d: datetime.date, stadium: int, race: int) -> dict:

        self.__logger.debug(f'{sys._getframe().f_code.co_name} called')
        # validation
        self.__validate_args(d, stadium, race)
        # format
        d = d.strftime('%Y%m%d')
        stdm = str(stadium).zfill(2)
        # get data and return the parsed object
        return self.__baseget(
            f'{self.__base_url}/racelist?rno={race}&jcd={stdm}&hd={d}',
            parsers.parse_html_racelist
        )

    def get_odds_win_placeshow(
        self,
        d: datetime.date,
        stadium: int,
        race: int
    ) -> dict:

        self.__logger.debug(f'{sys._getframe().f_code.co_name} called')
        # validation
        self.__validate_args(d, stadium, race)
        # format
        d = d.strftime('%Y%m%d')
        stdm = str(stadium).zfill(2)
        # get data and return the parsed object
        return self.__baseget(
            f'{self.__base_url}/oddstf?rno={race}&jcd={stdm}&hd={d}',
            parsers.parse_html_oddstf
        )

    def get_odds_quinellaplace(
        self,
        d: datetime.date,
        stadium: int,
        race: int
    ) -> dict:

        self.__logger.debug(f'{sys._getframe().f_code.co_name} called')
        # validation
        self.__validate_args(d, stadium, race)
        # format
        d = d.strftime('%Y%m%d')
        stdm = str(stadium).zfill(2)
        # get data and return the parsed object
        return self.__baseget(
            f'{self.__base_url}/oddsk?rno={race}&jcd={stdm}&hd={d}',
            parsers.parse_html_oddsk
        )

    def get_odds_exacta_quinella(
        self,
        d: datetime.date,
        stadium: int,
        race: int
    ) -> dict:

        self.__logger.debug(f'{sys._getframe().f_code.co_name} called')
        # validation
        self.__validate_args(d, stadium, race)
        # format
        d = d.strftime('%Y%m%d')
        stdm = str(stadium).zfill(2)
        # get data and return the parsed object
        return self.__baseget(
            f'{self.__base_url}/odds2tf?rno={race}&jcd={stdm}&hd={d}',
            parsers.parse_html_odds2tf
        )

    def get_odds_trifecta(
        self,
        d: datetime.date,
        stadium: int,
        race: int
    ) -> dict:

        self.__logger.debug(f'{sys._getframe().f_code.co_name} called')
        # validation
        self.__validate_args(d, stadium, race)
        # format
        d = d.strftime('%Y%m%d')
        stdm = str(stadium).zfill(2)
        # get data and return the parsed object
        return self.__baseget(
            f'{self.__base_url}/odds3t?rno={race}&jcd={stdm}&hd={d}',
            parsers.parse_html_odds3t
        )

    def get_odds_trio(
        self,
        d: datetime.date,
        stadium: int,
        race: int
    ) -> dict:

        self.__logger.debug(f'{sys._getframe().f_code.co_name} called')
        # validation
        self.__validate_args(d, stadium, race)
        # format
        d = d.strftime('%Y%m%d')
        stdm = str(stadium).zfill(2)
        # get data and return the parsed object
        return self.__baseget(
            f'{self.__base_url}/odds3f?rno={race}&jcd={stdm}&hd={d}',
            parsers.parse_html_odds3f
        )

    def get_just_before_info(
        self,
        d: datetime.date,
        stadium: int,
        race: int
    ) -> dict:

        self.__logger.debug(f'{sys._getframe().f_code.co_name} called')
        # validation
        self.__validate_args(d, stadium, race)
        # format
        d = d.strftime('%Y%m%d')
        stdm = str(stadium).zfill(2)
        # get data and return the parsed object
        return self.__baseget(
            f'{self.__base_url}/beforeinfo?rno={race}&jcd={stdm}&hd={d}',
            parsers.parse_html_beforeinfo
        )

    def get_race_result(
        self,
        d: datetime.date,
        stadium: int,
        race: int
    ) -> dict:

        self.__logger.debug(f'{sys._getframe().f_code.co_name} called')
        # validation
        self.__validate_args(d, stadium, race)
        # format
        d = d.strftime('%Y%m%d')
        stdm = str(stadium).zfill(2)
        # get data and return the parsed object
        return self.__baseget(
            f'{self.__base_url}/raceresult?rno={race}&jcd={stdm}&hd={d}',
            parsers.parse_html_raceresult
        )
