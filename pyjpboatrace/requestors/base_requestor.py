from abc import ABCMeta, abstractmethod
from requests.models import Response


class BaseRequestor(metaclass=ABCMeta):
    @abstractmethod
    def get(self, url: str) -> Response:
        raise NotImplementedError
