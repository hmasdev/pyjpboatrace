from abc import ABCMeta, abstractmethod
from requests.models import Response


class BaseRequestor(metaclass=ABCMeta):
    @abstractmethod
    def get(self, url: str) -> Response:
        raise NotImplementedError

    @abstractmethod
    def post(self, url: str, data: dict = {}) -> Response:
        raise NotImplementedError

    def __enter__(self):
        return self

    def __exit__(self):
        self.close()

    def __del__(self):
        self.close()

    def close(self):
        pass
