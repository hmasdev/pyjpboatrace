from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logging import getLogger

from ..user_information import UserInformation
from .boatracejp import check_login_status, login
from ..const import IBMBRACEORJP

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
    # TODO when failed
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
          .send_keys(user.vote_pass)

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
    # visit
    # TODO when failed
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
          .send_keys(user.vote_pass)

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
