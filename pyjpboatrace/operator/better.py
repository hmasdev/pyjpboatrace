from ..actions.ibmbraceorjp import bet
from .base import BaseOperator, DriverCheckMixin


class BettingOperator(BaseOperator, DriverCheckMixin):

    def do(
        self,
        stadium: int,
        race: int,
        betdict: dict,
        timeout: int = 15,
    ) -> bool:
        self._check_driver()
        return bet(
            stadium,
            race,
            betdict,
            driver=self._driver,
            user=self._user,
            timeout=timeout,
            logger=self._logger,
        )
