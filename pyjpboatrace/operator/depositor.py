from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base import BaseOperator, DriverCheckMixin
from .static import visit_ibmbraceorjp


class DepositOperator(BaseOperator, DriverCheckMixin):

    def do(
        self,
        depo_amt_unit_thousands_yen: int,
        timeout: int = 15,
    ) -> None:
        """To deposit money.

        Args:
            depo_amt_unit_thousands_yen (int): the amount of deposit.
            timeout (int, optional): timeout parameter. Defaults to 15.

        Raises:
            UnableActionException:
                Occurred when driver is not Chrome, Firefox or Edge.
        """
        self._check_driver()
        return self.__deposit(
            depo_amt_unit_thousands_yen,
            timeout=timeout,
        )

    def __deposit(
        self,
        depo_amt_unit_thousands_yen: int,
        timeout: int = 15,
    ):
        # visit
        visit_ibmbraceorjp(self._user, self._driver, timeout)

        # click deposit/withdraw
        WebDriverWait(self._driver, timeout).until(EC.presence_of_element_located((By.ID, 'gnavi01')))  # noqa
        self._driver.find_element(By.ID, 'gnavi01').click()

        WebDriverWait(self._driver, timeout).until(EC.presence_of_element_located((By.ID, 'charge')))  # noqa
        self._driver.find_element(By.ID, 'charge').click()

        # input
        WebDriverWait(self._driver, timeout).until(EC.presence_of_element_located((By.ID, 'chargeInstructAmt')))  # noqa
        self._driver.find_element(By.ID, 'chargeInstructAmt')\
            .send_keys(str(depo_amt_unit_thousands_yen))

        WebDriverWait(self._driver, timeout).until(EC.presence_of_element_located((By.ID, 'chargeBetPassword')))  # noqa
        self._driver.find_element(By.ID, 'chargeBetPassword')\
                    .send_keys(self._user.vote_pass)

        # press button
        WebDriverWait(self._driver, timeout).until(EC.presence_of_element_located((By.ID, 'executeCharge')))  # noqa
        self._driver.find_element(By.ID, 'executeCharge')\
            .click()

        WebDriverWait(self._driver, timeout).until(EC.presence_of_element_located((By.ID, 'ok')))  # noqa
        self._driver.find_element(By.ID, 'ok')\
            .click()
