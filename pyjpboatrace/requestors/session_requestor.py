import requests
from requests.models import Response
import time
from ..config import RequestorConfig
from .base_requestor import BaseRequestor

# TODO interval function to Mixin


class SessionRequestor(BaseRequestor):

    def __init__(self, interval_time=RequestorConfig.interval_time):

        # set config
        self.interval_time = interval_time
        self.previous_called = 0

        # create session
        self.__session = requests.Session()

    def get(self, url: str) -> Response:
        # get
        time.sleep(max(0, 1-time.time()+self.previous_called))
        http_response = self.__session.get(url, cookies=self.__session.cookies)
        self.previous_called = time.time()
        return http_response

    def post(self, url: str, data: dict = {}) -> Response:
        # post
        time.sleep(max(0, 1-time.time()+self.previous_called))
        http_response = self.__session.post(
            url,
            data=data,
            cookies=self.__session.cookies
        )
        self.previous_called = time.time()
        return http_response
