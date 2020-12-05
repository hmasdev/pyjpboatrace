from abc import ABCMeta, abstractmethod


class BaseRequestor(metaclass=ABCMeta):
    @abstractmethod
    def get(self, url: str) -> str:
        raise NotImplementedError
