from ..actions.ibmbraceorjp import get_bet_limit
from .base import BaseOperator, DriverCheckMixin


class BettingLimitCheckOperator(BaseOperator, DriverCheckMixin):

    def do(
        self,
        timeout: int = 15,
    ) -> int:
        self._check_driver()
        return get_bet_limit(
            driver=self._driver,
            user=self._user,
            timeout=timeout,
            logger=self._logger,
        )
