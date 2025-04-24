from logging import Logger, getLogger

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .const import BOATRACEJP_LOGIN_URL, BOATRACEJP_LOGOUT_URL, BOATRACEJP_MAIN_URL
from .exceptions import LoginFailException
from .user_information import UserInformation

# TODO error handling : failed to read
_logger: Logger = getLogger(__name__)


def login(
    driver: webdriver.remote.webdriver.WebDriver,
    user: UserInformation,
    timeout: int = 15,
    logger: Logger = _logger,
) -> bool:
    """Login to boatrace.jp

    Args:
        driver (webdriver.remote.webdriver.WebDriver): webdriver.
        user (UserInformation): User information.
        timeout (int, optional): Timeout parameter. Defaults to 15.
        logger (Logger, optional): logger. Defaults to getLogger(__name__).

    Raises:
        ValueError: Occurred when user.userid is None.
        ValueError: Occurred when user.pin is None.
        ValueError: Occurred when user.auth_pass is None.
        LoginFailException: Occurred when login failure.

    Returns:
        bool: Whether login is succeeded.

    NOTE:
        Behavior:
            Return True when login is succeeded;
            Raise LoginFailException when login is failed.
    """
    # validate
    if user.userid is None:
        raise ValueError('User ID is not set.')
    if user.pin is None:
        raise ValueError('PIN is not set.')
    if user.auth_pass is None:
        raise ValueError('Authentification password is not set.')

    # get
    driver.get(BOATRACEJP_LOGIN_URL)

    # send keys
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.NAME, 'in_KanyusyaNo'))
    )
    driver.find_element(By.CSS_SELECTOR, 'input[name="in_KanyusyaNo"]')\
          .send_keys(user.userid)
    logger.debug('put userid')

    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.NAME, 'in_AnsyoNo'))
    )
    driver.find_element(By.CSS_SELECTOR, 'input[name="in_AnsyoNo"]')\
          .send_keys(user.pin)
    logger.debug('put user pin')

    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.NAME, 'in_PassWord'))
    )
    driver.find_element(By.CSS_SELECTOR, 'input[name="in_PassWord"]')\
          .send_keys(user.auth_pass)
    logger.debug('put authentification password')

    # press button
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'is-type3_2'))
    )
    driver.find_element(By.CSS_SELECTOR, 'button[class="btn is-type3_2"]')\
          .click()
    logger.debug('Pressed login button')

    is_successed = check_login_status(driver)

    if not is_successed:
        raise LoginFailException()

    return is_successed


def logout(
    driver: webdriver.remote.webdriver.WebDriver,
    logger: Logger = _logger,
) -> bool:
    """Logout from boatrace.jp

    Args:
        driver (webdriver.remote.webdriver.WebDriver): webdriver
        logger (Logger, optional): logger. Defaults to getLogger(__name__).

    Returns:
        bool: Whether logout is succeeded.
    """
    # logout
    driver.get(BOATRACEJP_LOGOUT_URL)
    return not check_login_status(driver)


def check_login_status(
    driver: webdriver.remote.webdriver.WebDriver,
    logger: Logger = _logger,
) -> bool:
    """[summary]

    Args:
        driver (webdriver.remote.webdriver.WebDriver): webdriver
        logger (Logger, optional): logger. Defaults to getLogger(__name__).

    Returns:
        bool: Whether you are loggined in boatrace.jp
    """
    # get
    driver.get(BOATRACEJP_MAIN_URL)

    if driver.find_elements(By.CLASS_NAME, 'is-logout1'):
        return True
    else:
        return False
