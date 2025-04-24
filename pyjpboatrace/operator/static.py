from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ..certification import check_login_status, login
from ..const import IBMBRACEORJP
from ..user_information import UserInformation


def visit_ibmbraceorjp(
    user: UserInformation,
    driver: webdriver.remote.webdriver.WebDriver,
    timeout: int = 15,
) -> bool:
    """Visit and login to im.mbrace.or.jp.

    Args:
        user (UserInformation): user information
        driver (webdriver.remote.webdriver.WebDriver): webdriver
        timeout (int, optional): timeout parameter. Defaults to 15.

    Returns:
        bool: whether login is succeeded.
    """

    # check
    if not check_login_status(driver):
        login(driver, user, timeout)

    # visit
    driver.get(IBMBRACEORJP)

    # check
    return driver.title == 'トップ - BOAT RACE インターネット投票'


def get_bet_limit(
    user: UserInformation,
    driver: webdriver.remote.webdriver.WebDriver,
    timeout: int = 15
) -> int:
    """Get the amount of deposit.

    Args:
        user (UserInformation): user information.
        driver (webdriver.remote.webdriver.WebDriver): webdriver
        timeout (int, optional): timeout parameter. Defaults to 15.

    Returns:
        int: the amount of deposit.
    """

    # visit
    visit_ibmbraceorjp(user, driver, timeout)

    # get vote limit
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.ID, 'currentBetLimitAmount')))  # noqa
    limit = driver.find_element(By.ID, 'currentBetLimitAmount').text

    return int(limit.replace(',', ''))
