from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logging import getLogger

from ..user_information import UserInformation
from ..const import BOATRACEJP_MAIN_URL
from ..const import BOATRACEJP_LOGIN_URL, BOATRACEJP_LOGOUT_URL
from ..exceptions import LoginFailException

# TODO error handling : failed to read


def login(
    driver: webdriver.remote.webdriver.WebDriver,
    user: UserInformation,
    timeout: int = 15,
    logger=getLogger(__name__)
) -> bool:
    # get
    driver.get(BOATRACEJP_LOGIN_URL)

    # send keys
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.NAME, 'in_KanyusyaNo'))
    )
    driver.find_element_by_css_selector('input[name="in_KanyusyaNo"]')\
          .send_keys(user.userid)
    logger.debug('put userid')

    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.NAME, 'in_AnsyoNo'))
    )
    driver.find_element_by_css_selector('input[name="in_AnsyoNo"]')\
          .send_keys(user.pin)
    logger.debug('put user pin')

    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.NAME, 'in_PassWord'))
    )
    driver.find_element_by_css_selector('input[name="in_PassWord"]')\
          .send_keys(user.auth_pass)
    logger.debug('put authentification password')

    # press button
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'is-type3_2'))
    )
    driver.find_element_by_css_selector('button[class="btn is-type3_2"]')\
          .click()
    logger.debug('Pressed login button')

    is_successed = check_login_status(driver)

    if not is_successed:
        raise LoginFailException()

    return is_successed


def logout(
    driver: webdriver.remote.webdriver.WebDriver,
    logger=getLogger(__name__)
) -> bool:
    # logout
    driver.get(BOATRACEJP_LOGOUT_URL)
    return not check_login_status(driver)


def check_login_status(
    driver: webdriver.remote.webdriver.WebDriver,
    logger=getLogger(__name__)
) -> bool:
    # get
    driver.get(BOATRACEJP_MAIN_URL)

    if driver.find_elements_by_class_name('is-logout1'):
        return True
    else:
        return False
