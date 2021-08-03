from ..actions.ibmbraceorjp import deposit
from .base import BaseOperator, DriverCheckMixin


class DepositOperator(BaseOperator, DriverCheckMixin):

    def do(
        self,
        depo_amt_unit_thousands_yen: int,
        timeout: int = 15,
    ) -> bool:
        self._check_driver()
        return deposit(
            depo_amt_unit_thousands_yen,
            driver=self._driver,
            user=self._user,
            timeout=timeout,
            logger=self._logger,
        )
