from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ..exceptions import ZeroDepositException
from .base import BaseOperator, DriverCheckMixin
from .static import get_bet_limit, visit_ibmbraceorjp


class WithdrawOperator(BaseOperator, DriverCheckMixin):

    def do(
        self,
        timeout: int = 15,
        raise_validation_error: bool = False,
    ) -> bool:
        """To withdraw deposit.

        Args:
            timeout (int, optional): timeout parameter. Defaults to 15.
            raise_validation_error (bool, optional): whether raise validation error. Defaults to False.

        Raises:
            ValueError:
                Occurred when raise_validation_error is True and the vote password is not set.
            ZeroDepositException:
                Occurred when no deposit.
            UnableActionException:
                Occurred when driver is not Chrome, Firefox or Edge.
        """  # noqa
        self._check_driver()
        return self.__withdraw(
            timeout=timeout,
            raise_validation_error=raise_validation_error,
        )

    def __withdraw(
        self,
        timeout: int = 15,
        raise_validation_error: bool = False,
    ):
        # validation
        if self._user.vote_pass is None:
            if raise_validation_error:
                raise ValueError('Vote password is not set.')
            self._logger.error('Vote password is not set.')
            return None

        # get current bet limit
        current_limit = get_bet_limit(
            self._user,
            self._driver,
            timeout,
        )
        if current_limit == 0:
            # TODO add test
            raise ZeroDepositException('Current deposit is zero.')

        # visit
        visit_ibmbraceorjp(self._user, self._driver, timeout)

        # click deposit/withdraw
        WebDriverWait(self._driver, timeout).until(EC.presence_of_element_located((By.ID, 'gnavi01')))  # noqa
        self._driver.find_element(By.ID, 'gnavi01').click()

        WebDriverWait(self._driver, timeout).until(EC.presence_of_element_located((By.ID, 'account')))  # noqa
        self._driver.find_element(By.ID, 'account').click()

        # input
        WebDriverWait(self._driver, timeout).until(EC.presence_of_element_located((By.ID, 'accountBetPassword')))  # noqa
        self._driver.find_element(By.ID, 'accountBetPassword')\
            .send_keys(self._user.vote_pass)

        # press button
        WebDriverWait(self._driver, timeout).until(EC.presence_of_element_located((By.ID, 'executeAccount')))  # noqa
        self._driver.find_element(By.ID, 'executeAccount')\
            .click()

        WebDriverWait(self._driver, timeout).until(EC.presence_of_element_located((By.ID, 'ok')))  # noqa
        self._driver.find_element(By.ID, 'ok')\
            .click()
