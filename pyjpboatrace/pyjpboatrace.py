import datetime
from logging import getLogger
import sys

from bs4 import BeautifulSoup
from selenium import webdriver

from . import parsers
from .exceptions import NoDataException, UnableActionException
from .const import BOATRACEJP_BASE_URL, NUM_RACES, NUM_STADIUMS
from pyjpboatrace.drivers import create_httpget_driver, HTTPGetDriver
from .user_information import UserInformation
from .actions import boatracejp
from .actions import ibmbraceorjp

class PyJPBoatrace(object):

    def __init__(
        self,
        driver: webdriver.remote.webdriver.WebDriver = create_httpget_driver(),
        user_information: UserInformation = None,
        logger=getLogger(__name__),
        use_cache = False
    ):
        self.__driver = driver
        self.__user_information = user_information
        self.__logger = logger
        self.__use_cache = use_cache

        if self.__are_enable_actions():
            boatracejp.login(self.__driver, self.__user_information)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __del__(self):
        self.close()

    def close(self):
        if self.__are_enable_actions():
            boatracejp.logout(self.__driver)
        self.__driver.close()

    def __are_enable_actions(self):
        if isinstance(self.__driver, HTTPGetDriver):
            self.__logger.warning(
                f'self.__driver is an instance of {HTTPGetDriver.__name__}. '
                'However, it must be an instance of '
                'selenium.webdriver.remote.webdriver.WebDriver, '
                f'not {HTTPGetDriver.__name__}, '
                'if you want to execute actions '
                'against boatrace.jp and ib.mbrace.or.jp'
            )
            return False
        if self.__user_information is None:
            self.__logger.warning(
                'self.__user_information is None.'
                'It is necessary for actions '
                'against boatrace.jp and ib.mbrace.or.jp'
            )
            return False
        return True

    def __baseget(self, url: str, parser,use_cache:bool = False) -> dict:

        self.__logger.debug(f'Start requesting {url}')
        self.__driver.get(url,use_cache)
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
            f'{BOATRACEJP_BASE_URL}/index?hd={d}',
            parsers.parse_html_index,use_cache=self.__use_cache
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
            f"{BOATRACEJP_BASE_URL}/raceindex?jcd={stdm}&hd={d}",
            parsers.parse_html_raceindex,use_cache=self.__use_cache
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
            f'{BOATRACEJP_BASE_URL}/racelist?rno={race}&jcd={stdm}&hd={d}',
            parsers.parse_html_racelist,use_cache=self.__use_cache
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
            f'{BOATRACEJP_BASE_URL}/oddstf?rno={race}&jcd={stdm}&hd={d}',
            parsers.parse_html_oddstf,use_cache=self.__use_cache
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
            f'{BOATRACEJP_BASE_URL}/oddsk?rno={race}&jcd={stdm}&hd={d}',
            parsers.parse_html_oddsk,use_cache=self.__use_cache
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
            f'{BOATRACEJP_BASE_URL}/odds2tf?rno={race}&jcd={stdm}&hd={d}',
            parsers.parse_html_odds2tf,use_cache=self.__use_cache
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
            f'{BOATRACEJP_BASE_URL}/odds3t?rno={race}&jcd={stdm}&hd={d}',
            parsers.parse_html_odds3t,use_cache=self.__use_cache
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
            f'{BOATRACEJP_BASE_URL}/odds3f?rno={race}&jcd={stdm}&hd={d}',
            parsers.parse_html_odds3f,use_cache=self.__use_cache
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
            f'{BOATRACEJP_BASE_URL}/beforeinfo?rno={race}&jcd={stdm}&hd={d}',
            parsers.parse_html_beforeinfo,use_cache=self.__use_cache
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
            f'{BOATRACEJP_BASE_URL}/raceresult?rno={race}&jcd={stdm}&hd={d}',
            parsers.parse_html_raceresult,use_cache=self.__use_cache
        )

    def deposit(self, num_of_thousands_yen: int) -> None:
        # preparation
        if not self.__are_enable_actions():
            # TODO add test
            raise UnableActionException()

        # deposit
        ibmbraceorjp.deposit(
            num_of_thousands_yen,
            driver=self.__driver,
            user=self.__user_information
        )

    def get_bet_limit(self) -> int:
        # preparation
        if not self.__are_enable_actions():
            # TODO create exception
            raise Exception

        # deposit
        limit = ibmbraceorjp.get_bet_limit(
            driver=self.__driver,
            user=self.__user_information
        )

        return limit

    def withdraw(self) -> None:
        # preparation
        if not self.__are_enable_actions():
            # TODO add test
            raise UnableActionException()

        # deposit
        ibmbraceorjp.withdraw(
            driver=self.__driver,
            user=self.__user_information
        )

    def bet(
        self,
        place: int,
        race: int,
        trifecta_betting_dict: dict = {},
        trio_betting_dict: dict = {},
        exacta_betting_dict: dict = {},
        quinella_betting_dict: dict = {},
        quinellaplace_betting_dict: dict = {},
        win_betting_dict: dict = {},
        placeshow_betting_dict: dict = {},
    ) -> bool:
        # preparation
        if not self.__are_enable_actions():
            # TODO add test
            raise UnableActionException()

        # create bet dict
        betdict = {
            'trifecta': trifecta_betting_dict,
            'trio': trio_betting_dict,
            'exacta': exacta_betting_dict,
            'quinella': quinella_betting_dict,
            'quinellaplace': quinellaplace_betting_dict,
            'win': win_betting_dict,
            'placeshow': placeshow_betting_dict,
        }

        # deposit
        return ibmbraceorjp.bet(
            place=place,
            race=race,
            betdict=betdict,
            driver=self.__driver,
            user=self.__user_information
        )
