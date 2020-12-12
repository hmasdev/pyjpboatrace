from abc import ABCMeta, abstractmethod
from requests.models import Response


class BaseRequestor(metaclass=ABCMeta):
    @abstractmethod
    def get(self, url: str) -> Response:
        raise NotImplementedError

    @abstractmethod
    def post(self, url: str, data: dict = {}) -> Response:
        raise NotImplementedError
