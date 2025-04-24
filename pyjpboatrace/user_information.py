import json
import os
from getpass import getpass
from logging import Logger, getLogger
from typing import Optional

_logger: Logger = getLogger(__name__)


class UserInformation:
    """ Use-information container class

    - userid
    - pin
    - auth_pass
    - vote_pass

    """

    def __init__(
        self,
        userid: Optional[str] = None,
        pin: Optional[str] = None,
        auth_pass: Optional[str] = None,
        vote_pass: Optional[str] = None,  # TODO rename vote_pass -> bet_pass
        json_file: Optional[str] = None,
        logger: Logger = _logger,
    ):
        # preparation
        self.userid: Optional[str] = None
        self.pin: Optional[str] = None
        self.auth_pass: Optional[str] = None
        self.vote_pass: Optional[str] = None

        # load json
        if json_file is not None and os.path.exists(json_file):
            with open(json_file, 'r', encoding='utf-8-sig') as f:
                dic = json.load(f)
            self.userid = dic.get('userid', None)
            self.pin = dic.get('pin', None)
            self.auth_pass = dic.get('auth_pass', None)
            self.vote_pass = dic.get('vote_pass', None)

        if userid is not None:
            self.userid = userid
        if pin is not None:
            self.pin = pin
        if auth_pass is not None:
            self.auth_pass = auth_pass
        if vote_pass is not None:
            self.vote_pass = vote_pass

        if self.userid is None:
            self.userid = input('Input your id: ')
        if self.pin is None:
            self.pin = getpass(u'Input pin (暗証番号): ')
        if self.auth_pass is None:
            self.auth_pass = getpass(
                u'Input authentification password (認証用パスワード): '
            )
        if self.vote_pass is None:
            self.vote_pass = getpass(
                u'Input vote password (投票用パスワード): '
            )
