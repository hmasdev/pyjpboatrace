import requests
import time
import os
import json
from bs4 import BeautifulSoup
from getpass import getpass
from logging import getLogger

from ..config import RequestorConfig
from .base_requestor import BaseRequestor
from ..exceptions import LoginFailException


class BoatracejpRequestor(BaseRequestor):

    # TODO move these urls outside
    __main_url = 'https://www.boatrace.jp'
    __login_url = 'https://www.boatrace.jp/owpc/pc/login'

    def __init__(
        self,
        userid: str = None,
        pin: str = None,
        auth_pass: str = None,
        vote_pass: str = None,
        login_info_json: str = None,
        interval_time=RequestorConfig.interval_time,
        logger=getLogger()
    ):

        # set config
        self.interval_time = interval_time
        self.previous_called = 0
        self.logger = logger

        # extract login info
        self.__login_info = {
            'userid': None,
            'pin': None,
            'auth_pass': None,
            'vote_pass': None,
        }

        if login_info_json is not None:
            if os.path.exists(login_info_json):
                with open(login_info_json, 'r', encoding='utf-8') as f:
                    self.logger.debug(
                        f'Found {login_info_json}. Set login info to them.'
                    )
                    self.__login_info = json.load(f)
        if userid is not None:
            self.logger.debug('userid is given. Set userid to the given one.')
            self.__login_info['userid'] = userid
        if pin is not None:
            self.logger.debug('pin is given. Set pin to the given one.')
            self.__login_info['pin'] = pin
        if auth_pass is not None:
            self.logger.debug(
                'auth_pass is given. Set auth_pass to the given one.'
            )
            self.__login_info['auth_pass'] = auth_pass
        if vote_pass is not None:
            self.logger.debug(
                'vote_pass is given. Set vote_pass to the given one.'
            )
            self.__login_info['vote_pass'] = vote_pass

        # input login info
        if self.__login_info['userid'] is None:
            self.__login_info['userid'] = input(u"Input User No.(加入者番号):")
        if self.__login_info['pin'] is None:
            self.__login_info['pin'] = getpass(u'Input PIN (暗証番号):')
        if self.__login_info['auth_pass'] is None:
            self.__login_info['auth_pass'] = getpass(
                u'Input Authentification Password (認証用パスワード):'
            )
        if self.__login_info['vote_pass'] is None:
            self.__login_info['vote_pass'] = getpass(
                u'Input Vote Password (投票用パスワード):'
            )

        # get session
        self.__session = requests.Session()

        # try login
        self.logger.info('Trying to login...')
        if not self.__login():
            raise LoginFailException(
                f'Failed to login into {self.__login_url}'
            )
        self.logger.info('Succeeded in login.')

    def get(self, url: str):
        time.sleep(max(0, 1-time.time()+self.previous_called))
        http_response = self.__session.get(url)
        self.previous_called = time.time()
        return http_response.text

    def __login(self):
        # preparation
        html = self.__session.get(self.__login_url).text
        soup = BeautifulSoup(html, 'html.parser')
        self.logger.debug(f'HTTP GET {self.__login_url}')

        # get token
        css_selector = 'input[name="org.apache.struts.taglib.html.TOKEN"]'
        token = soup.select_one(css_selector)['value']
        self.logger.debug(f'Get TOKEN from {self.__login_url}')

        # get orteusPrevForward
        orteusPF = soup.select_one('input[name="orteusPrevForward"]')['value']
        self.logger.debug(
            f'Get the value of orteusPrevForward from {self.__login_url}'
        )

        # payload
        payload = {
            'org.apache.struts.taglib.html.TOKEN': token,
            'orteusPrevForward': orteusPF,
            'orteusElements': True,
            'com.nec.jp.orteusActionMethod.login': 'controlLogin',
            'login': 'Submit',
            'in_AuthAfterUrl': '/',
            'in_KanyusyaNo': self.__login_info['userid'],
            'in_AnsyoNo': self.__login_info['pin'],
            'in_PassWord': self.__login_info['auth_pass']
        }

        # login
        self.__session.post(self.__login_url, data=payload)
        self.logger.debug('Tried to login')

        return self.check_login_status()

    def check_login_status(self):
        # try to get main page
        html = self.__session.get(self.__main_url).text
        self.logger.debug(f'HTTP GET {self.__main_url}')
        # extract spans related to login information
        soup = BeautifulSoup(html, 'html.parser')
        spans = soup.select(' > '.join([
            'div.headerMember',
            'div.headerMember_inner',
            'p.headerMember_info',
            'span'
        ]))

        if spans and len(spans) >= 2:
            userid = ''.join(spans[1].text.replace('加入者番号:', '').split())
            return userid == self.__login_info['userid']
        else:
            return False
