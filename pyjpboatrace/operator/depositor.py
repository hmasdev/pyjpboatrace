from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .base import BaseOperator, DriverCheckMixin
from .static import visit_ibmbraceorjp


class DepositOperator(BaseOperator, DriverCheckMixin):

    def do(
        self,
        depo_amt_unit_thousands_yen: int,
        timeout: int = 15,
        raise_validation_error: bool = False,
    ) -> None:
        """To deposit money.

        Args:
            depo_amt_unit_thousands_yen (int): the amount of deposit.
            timeout (int, optional): timeout parameter. Defaults to 15.
            raise_validation_error (bool, optional): whether raise validation error. Defaults to False.

        Raises:
            ValueError:
                Occurred when raise_validation_error is True and the vote password is not set.
            UnableActionException:
                Occurred when driver is not Chrome, Firefox or Edge.
        """  # noqa
        self._check_driver()
        return self.__deposit(
            depo_amt_unit_thousands_yen,
            timeout=timeout,
            raise_validation_error=raise_validation_error,
        )

    def __deposit(
        self,
        depo_amt_unit_thousands_yen: int,
        timeout: int = 15,
        raise_validation_error: bool = False,
    ):
        # validation
        if self._user.vote_pass is None:
            if raise_validation_error:
                raise ValueError('Vote password is not set.')
            self._logger.error('Vote password is not set.')
            return None

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
