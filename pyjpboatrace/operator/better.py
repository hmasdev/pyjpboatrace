import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ..exceptions import (
    InactiveRace,
    InactiveStadium,
    InsufficientDepositException,
    ZeroDepositException,
)
from ..validator import validate_race, validate_stadium
from .base import BaseOperator, DriverCheckMixin
from .static import get_bet_limit, visit_ibmbraceorjp


class BettingOperator(BaseOperator, DriverCheckMixin):
    """To bet.
    """

    def do(
        self,
        stadium: int,
        race: int,
        betdict: dict,
        timeout: int = 15,
        raise_validation_error: bool = False,
    ) -> bool:
        """To bet money on the race.

        Args:
            stadium (int): stadium no.
            race (int): race no.
            betdict (dict): betting target dictionary.
            timeout (int, optional): timeout parameter. Defaults to 15.
            raise_validation_error (bool, optional): whether raise validation error. Defaults to False.

        Raises:
            ValueError: Occurred when raise_validation_error is True and the vote password is not set.
            ValueError: Occurred when invalid stadium no. given.
            ValueError: Occurred when invalid race no. given.
            UnableActionException:
                Occurred when driver is not Chrome, Firefox or Edge.
            ZeroDepositException:
                Occurred when no deposit.
            InactiveStadium:
                Occurred when stadium no. is valid but no races are there.
            InactiveRace:
                Occurred when race no. is valid but the race is probabily over.
            InsufficientDepositException:
                Occurred when the sum of your bet is greater than deposit.

        Returns:
            bool: whether betting is succeeded

        NOTE:
            betdict keys:
                'win',
                'placeshow',
                'exacta',
                'quinella',
                'quinellaplace',
                'trifecta',
                'trio',

        TODO: to create the data structure for betdict.
        """  # noqa
        self._check_driver()
        validate_race(race)
        validate_stadium(stadium)
        return self.__bet(
            stadium,
            race,
            betdict,
            timeout=timeout,
            raise_validation_error=raise_validation_error,
        )

    def __bet(
        self,
        stadium: int,  # TODO rename stadium -> stadium
        race: int,
        betdict: dict,
        timeout: int = 15,
        raise_validation_error: bool = False,
    ) -> bool:
        # validation
        if self._user.vote_pass is None:
            if raise_validation_error:
                raise ValueError('Vote password is not set.')
            self._logger.error('Vote password is not set.')
            return False

        # visit
        visit_ibmbraceorjp(self._user, self._driver, timeout)

        # TODO when limit is not enough
        limit = get_bet_limit(self._user, self._driver, timeout)
        if limit == 0:
            # TODO add test
            raise ZeroDepositException('Current deposit is zero.')

        # click stadium
        WebDriverWait(self._driver, timeout).until(EC.presence_of_element_located((By.ID, f'jyo{stadium:02d}')))  # noqa
        element = self._driver.find_element(By.ID, f'jyo{stadium:02d}')
        if 'borderNone' in element.get_attribute('class'):  # type: ignore  # noqa
            # invalid stadium case
            # TODO add test
            raise InactiveStadium(f'The stadium {stadium:02d} has not active races')  # noqa
        else:
            element.click()

        # click race
        WebDriverWait(self._driver, timeout).until(EC.presence_of_element_located((By.ID, f'selRaceNo{race:02d}')))  # noqa
        element = self._driver.find_element(By.ID, f'selRaceNo{race:02d}')
        if 'end' in element.get_attribute('class'):  # type: ignore  # noqa
            # invalid race case
            # TODO add test
            raise InactiveRace(f'Race{race:02d} in stadium {stadium:02d} has ended or is not hold.')  # noqa
        else:
            element.click()

        # create betting list
        # TODO make kinds constant
        amount: int = 0
        for kind_idx, kind in enumerate([
            'win',
            'placeshow',
            'exacta',
            'quinella',
            'quinellaplace',
            'trifecta',
            'trio',
        ]):
            bet_dict_for_kind = betdict.get(kind, None)

            # if not given
            if bet_dict_for_kind is None:
                self._logger.info(f'Skip betting {kind}')
                continue

            # click kind
            self._driver.find_element(By.ID, f'betkati{kind_idx+1}').click()
            time.sleep(1)

            # input bet
            for order, amt in bet_dict_for_kind.items():
                # TODO make sep constant
                sep = '=' if '=' in order else '-'
                boats = tuple(map(int, order.split(sep)))
                print(kind, order, amt)
                for boat_idx, boat in enumerate(boats):
                    self._driver.find_element(By.ID, f'regbtn_{boat}_{boat_idx+1}').click()  # noqa

                self._driver.find_element(By.ID, 'amount').send_keys('\b'*10)  # noqa
                self._driver.find_element(By.ID, 'amount').send_keys(amt//100)  # noqa
                self._driver.find_element(By.ID, 'regAmountBtn').click()

                amount = amount + amt

        # complete input
        self._driver.find_element(By.CLASS_NAME, 'btnSubmit').click()

        # insufficient depost
        if amount > limit:
            # TODO add test
            raise InsufficientDepositException(
                f'Your betting amount is {amount}, '
                f'but your current deposit is {limit}.'
            )

        # confirmation
        self._driver.find_element(By.ID, 'amount').send_keys(str(amount))
        self._driver.find_element(By.ID, 'pass').send_keys(self._user.vote_pass)  # noqa
        self._driver.find_element(By.ID, 'submitBet').click()
        self._driver.find_element(By.ID, 'ok').click()
        # TODO check whether amount is equal to the amount betted
        # TODO vote time limit comes during this function

        return True
