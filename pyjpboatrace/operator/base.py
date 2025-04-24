from abc import ABCMeta, abstractmethod
from logging import Logger, getLogger
from typing import Any

from selenium import webdriver

from ..exceptions import UnableActionException
from ..user_information import UserInformation

_logger: Logger = getLogger(__name__)


class BaseOperator(metaclass=ABCMeta):
    """Base class for operator
    """

    def __init__(
        self,
        user: UserInformation,
        driver: webdriver.remote.webdriver.WebDriver,
        logger: Logger = _logger,
    ):
        self._user = user
        self._driver = driver
        self._logger = logger

    @abstractmethod
    def do(self, *args, **kwargs) -> Any:
        raise NotImplementedError()


class DriverCheckMixin:

    def _check_driver(self):
        """Check whether self._driver is Chrome, Firefox or Edge

        Raises:
            UnableActionException: Occurred when self._driver is not Chrome, Firefox or Edge
        """  # noqa
        if not (
            isinstance(self._driver, webdriver.Chrome)
            or isinstance(self._driver, webdriver.Firefox)
            or isinstance(self._driver, webdriver.Edge)
        ):
            raise UnableActionException(
                "Given driver is not Chrome, Firefox or Edge. "
                "So the operator cannot do anything."
            )
