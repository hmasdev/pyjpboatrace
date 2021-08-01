import os
import pytest
from pyjpboatrace.user_information import UserInformation
from pyjpboatrace.drivers import create_chrome_driver, create_firefox_driver
# from pyjpboatrace.drivers import create_edge_driver  # TODO test edge driver
from pyjpboatrace.actions.boatracejp import login, check_login_status, logout
from pyjpboatrace.exceptions import LoginFailException

SECRETSJSON = './.secrets.json'


def get_user_info(secretsjson=SECRETSJSON):
    if os.path.exists(secretsjson):
        return UserInformation(json_file=secretsjson)
    else:
        return None


@pytest.mark.skipif(
    not os.path.exists(SECRETSJSON),
    reason=f'{SECRETSJSON} not found'
)
@pytest.mark.integrate
@pytest.mark.parametrize(
    'create_driver',
    (
        create_chrome_driver,
        create_firefox_driver,
        # create_edge_driver,
    )
)
def test_login_logout(create_driver):
    # preparation
    driver = create_driver()
    user = get_user_info()
    # pre-status
    assert not check_login_status(driver)
    # login
    assert login(driver, user)
    assert check_login_status(driver)
    # logout
    assert logout(driver)
    assert not check_login_status(driver)
    # quit
    driver.close()


@pytest.mark.integrate
@pytest.mark.parametrize(
    'create_driver',
    (
        create_chrome_driver,
        create_firefox_driver,
        # create_edge_driver,
    )
)
def test_login_wrong_pass(create_driver):
    # preparation
    driver = create_driver()
    user = UserInformation('a', 'b', 'c', 'd')
    # pre-status
    assert not check_login_status(driver)
    # login
    with pytest.raises(LoginFailException):
        login(driver, user)
    assert not check_login_status(driver)
    # quit
    driver.close()
