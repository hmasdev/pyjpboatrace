from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base import BaseOperator, DriverCheckMixin
from ..exceptions import ZeroDepositException
from .static import get_bet_limit, visit_ibmbraceorjp


class WithdrawOperator(BaseOperator, DriverCheckMixin):

    def do(
        self,
        timeout: int = 15,
    ) -> bool:
        """To withdraw deposit.

        Args:
            timeout (int, optional): timeout parameter. Defaults to 15.

        Raises:
            ZeroDepositException:
                Occurred when no deposit.
            UnableActionException:
                Occurred when driver is not Chrome, Firefox or Edge.
        """
        self._check_driver()
        return self.__withdraw(timeout=timeout,)

    def __withdraw(
        self,
        timeout: int = 15,
    ):
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
        WebDriverWait(self._driver, timeout).until(
            EC.presence_of_element_located((By.ID, 'gnavi01'))
        )
        self._driver.find_element_by_id('gnavi01').click()

        WebDriverWait(self._driver, timeout).until(
            EC.presence_of_element_located((By.ID, 'account'))
        )
        self._driver.find_element_by_id('account').click()

        # input
        WebDriverWait(self._driver, timeout).until(
            EC.presence_of_element_located((By.ID, 'accountBetPassword'))
        )
        self._driver.find_element_by_id('accountBetPassword')\
            .send_keys(self._user.vote_pass)

        # press button
        WebDriverWait(self._driver, timeout).until(
            EC.presence_of_element_located((By.ID, 'executeAccount'))
        )
        self._driver.find_element_by_id('executeAccount')\
            .click()

        WebDriverWait(self._driver, timeout).until(
            EC.presence_of_element_located((By.ID, 'ok'))
        )
        self._driver.find_element_by_id('ok')\
            .click()
