import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logging import getLogger

from ..user_information import UserInformation
from .boatracejp import check_login_status, login
from ..const import IBMBRACEORJP
from ..exceptions import InsufficientDepositException, ZeroDepositException
from ..exceptions import InactiveRace, InactiveStadium

# TODO error handling : wrong vote_pass
# TODO error handling : failed to read


def _visit_ibmbraceorjp(
    driver: webdriver.remote.webdriver.WebDriver,
    user: UserInformation,
    timeout: int = 15,
    logger=getLogger(__name__)
) -> bool:
    # check
    if not check_login_status(driver):
        login(driver, user, timeout)

    # visit
    driver.get(IBMBRACEORJP)

    # check
    return driver.title == 'トップ - BOAT RACE インターネット投票'


def get_bet_limit(
    driver: webdriver.remote.webdriver.WebDriver,
    user: UserInformation,
    timeout: int = 15,
    logger=getLogger(__name__)
) -> int:
    # visit
    _visit_ibmbraceorjp(driver, user, timeout, logger=logger)

    # get vote limit
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.ID, 'currentBetLimitAmount'))
    )
    limit = driver.find_element_by_id('currentBetLimitAmount').text

    return int(limit.replace(',', ''))


def deposit(
    depo_amt_unit_thousands_yen: int,
    driver: webdriver.remote.webdriver.WebDriver,
    user: UserInformation,
    timeout: int = 15,
    logger=getLogger(__name__)
):
    # visit
    # TODO when failed
    _visit_ibmbraceorjp(driver, user, timeout, logger)

    # click deposit/withdraw
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.ID, 'gnavi01'))
    )
    driver.find_element_by_id('gnavi01').click()

    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.ID, 'charge'))
    )
    driver.find_element_by_id('charge').click()

    # input
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.ID, 'chargeInstructAmt'))
    )
    driver.find_element_by_id('chargeInstructAmt')\
          .send_keys(str(depo_amt_unit_thousands_yen))

    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.ID, 'chargeBetPassword'))
    )
    driver.find_element_by_id('chargeBetPassword')\
          .send_keys(user.bet_pass)

    # press button
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.ID, 'executeCharge'))
    )
    driver.find_element_by_id('executeCharge')\
          .click()

    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.ID, 'ok'))
    )
    driver.find_element_by_id('ok')\
          .click()


def withdraw(
    driver: webdriver.remote.webdriver.WebDriver,
    user: UserInformation,
    timeout: int = 15,
    logger=getLogger(__name__)
):
    # get current bet limit
    current_limit = get_bet_limit(driver, user, timeout, logger)
    if current_limit == 0:
        # TODO add test
        raise ZeroDepositException('Current deposit is zero.')

    # visit
    _visit_ibmbraceorjp(driver, user, timeout, logger)

    # click deposit/withdraw
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.ID, 'gnavi01'))
    )
    driver.find_element_by_id('gnavi01').click()

    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.ID, 'account'))
    )
    driver.find_element_by_id('account').click()

    # input
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.ID, 'accountBetPassword'))
    )
    driver.find_element_by_id('accountBetPassword')\
          .send_keys(user.bet_pass)

    # press button
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.ID, 'executeAccount'))
    )
    driver.find_element_by_id('executeAccount')\
          .click()

    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.ID, 'ok'))
    )
    driver.find_element_by_id('ok')\
          .click()


def bet(
    place: int,  # TODO rename place -> stadium
    race: int,
    betdict: dict,
    driver: webdriver.remote.webdriver.WebDriver,
    user: UserInformation,
    timeout: int = 15,
    logger=getLogger(__name__)
) -> bool:
    # visit
    _visit_ibmbraceorjp(driver, user, timeout, logger)

    # TODO when limit is not enough
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.ID, 'currentBetLimitAmount'))
    )
    limit = int(
        driver.find_element_by_id('currentBetLimitAmount')
              .text
              .replace(',', '')
    )
    if limit == 0:
        # TODO add test
        raise ZeroDepositException('Current deposit is zero.')

    # click place
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.ID, f'jyo{place:02d}'))
    )
    element = driver.find_element_by_id(f'jyo{place:02d}')
    if 'borderNone' in element.get_attribute('class'):
        # invalid place case
        # TODO add test
        raise InactiveStadium(f'The stadium {place:02d} has not active races')
    else:
        element.click()

    # click race
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.ID, f'selRaceNo{race:02d}'))
    )
    element = driver.find_element_by_id(f'selRaceNo{race:02d}')
    if 'end' in element.get_attribute('class'):
        # invalid race case
        # TODO add test
        raise InactiveRace(
            f'Race{race:02d} in stadium {place:02d} has ended or is not hold.'
        )
    else:
        element.click()

    # create betting list
    # TODO make kinds constant
    amount = 0
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
            logger.info(f'Skip betting {kind}')
            continue

        # click kind
        driver.find_element_by_id(f'betkati{kind_idx+1}').click()
        time.sleep(1)

        # input bet
        for order, amt in bet_dict_for_kind.items():
            # TODO make sep constant
            sep = '=' if '=' in order else '-'
            boats = tuple(map(int, order.split(sep)))
            print(kind, order, amt)
            for boat_idx, boat in enumerate(boats):
                driver.find_element_by_id(
                    f'regbtn_{boat}_{boat_idx+1}'
                ).click()

            driver.find_element_by_id('amount').send_keys('\b'*10)  # TODO
            driver.find_element_by_id('amount').send_keys(amt//100)
            driver.find_element_by_id('regAmountBtn').click()

            amount = amount + amt

    # complete input
    driver.find_element_by_class_name('btnSubmit').click()

    # insufficient depost
    if amount > limit:
        # TODO add test
        raise InsufficientDepositException(
            f'Your betting amount is {amount}, '
            f'but your current deposit is {limit}.'
        )

    # confirmation
    driver.find_element_by_id('amount').send_keys(amount)
    driver.find_element_by_id('pass').send_keys(user.bet_pass)
    driver.find_element_by_id('submitBet').click()
    driver.find_element_by_id('ok').click()
    # TODO check whether amount is equal to the amount betted
    # TODO vote time limit comes during this function

    return True
