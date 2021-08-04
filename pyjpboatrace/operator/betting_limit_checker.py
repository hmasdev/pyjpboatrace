from .base import BaseOperator, DriverCheckMixin
from .static import get_bet_limit


class BettingLimitCheckOperator(BaseOperator, DriverCheckMixin):

    def do(
        self,
        timeout: int = 15,
    ) -> int:
        """To check the amount of money deposited.

        Args:
            timeout (int, optional): timeout parameter. Defaults to 15.

        Raises:
            UnableActionException:
                Occurred when driver is not Chrome, Firefox or Edge.

        Returns:
            int: the amount of deposited money
        """
        self._check_driver()
        return self.__get_bet_limit(timeout=timeout,)

    def __get_bet_limit(self, timeout: int = 15) -> int:
        return get_bet_limit(
            self._user,
            self._driver,
            timeout,
        )
