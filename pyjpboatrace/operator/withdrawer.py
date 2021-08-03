from ..actions.ibmbraceorjp import withdraw
from .base import BaseOperator, DriverCheckMixin


class WithdrawOperator(BaseOperator, DriverCheckMixin):

    def do(
        self,
        timeout: int = 15,
    ) -> bool:
        self._check_driver()
        return withdraw(
            driver=self._driver,
            user=self._user,
            timeout=timeout,
            logger=self._logger,
        )
