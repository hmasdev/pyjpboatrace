import os
import json
from getpass import getpass
from requests.models import Response
from logging import getLogger
from ..config import RequestorConfig
from .session_requestor import SessionRequestor

# TODO interval function to Mixin


class BoatraceRequestor(SessionRequestor):

    def __init__(
        self,
        userid: str = None,
        pin: str = None,
        auth_pass: str = None,
        vote_pass: str = None,
        login_info_json: str = None,
        interval_time=RequestorConfig.interval_time,
        logger=getLogger(__name__)
    ):
        # initialize
        super().__init__(interval_time=interval_time)
        self.logger = logger

        # extract login info
        self.__set_login_info(userid, pin, auth_pass,
                              vote_pass, login_info_json)

    def get(self, url: str) -> Response:
        return super().get(url=url)

    def post(
        self,
        url: str,
        data: dict = {},
        login_info_key_2_form_key: dict = {}
    ) -> Response:
        data_ = dict([item for item in data.items()])
        for key1, key2 in login_info_key_2_form_key.items():
            data_[key2] = self.__login_info[key1]
        return super().post(url, data=data_)

    def __set_login_info(
        self,
        userid: str = None,
        pin: str = None,
        auth_pass: str = None,
        vote_pass: str = None,
        login_info_json: str = None,
    ):
        # preparation
        self.__login_info = {
            'userid': None,
            'pin': None,
            'auth_pass': None,
            'vote_pass': None,
        }

        # extract
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
