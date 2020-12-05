import requests
import time
from ..config import RequestorConfig
from .base_requestor import BaseRequestor

# TODO interval function to Mixin


class Requestor(BaseRequestor):

    def __init__(self, interval_time=RequestorConfig.interval_time):
        self.interval_time = interval_time
        self.previous_called = 0

    def get(self, url: str) -> str:
        time.sleep(max(0, 1-time.time()+self.previous_called))
        http_response = requests.get(url)
        self.previous_called = time.time()
        return http_response.text
