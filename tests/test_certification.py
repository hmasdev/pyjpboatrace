import pytest

from pyjpboatrace.certification import check_login_status, login, logout
from pyjpboatrace.exceptions import LoginFailException
from pyjpboatrace.user_information import UserInformation

from ._driver_fixutures import driver_not_http_get_driver  # noqa
from ._utils import get_user_info


@pytest.mark.skipif(
    get_user_info() is None,
    reason='UserInformation not found'
)
@pytest.mark.integrate
def test_login_logout(driver_not_http_get_driver):  # noqa
    # preparation
    driver = driver_not_http_get_driver
    user = get_user_info()
    # pre-status
    assert not check_login_status(driver)
    # login
    assert login(driver, user)
    assert check_login_status(driver)
    # logout
    assert logout(driver)
    assert not check_login_status(driver)


@pytest.mark.integrate
def test_login_wrong_pass(driver_not_http_get_driver):  # noqa
    # preparation
    driver = driver_not_http_get_driver
    user = UserInformation('a', 'b', 'c', 'd')
    # pre-status
    assert not check_login_status(driver)
    # login
    with pytest.raises(LoginFailException):
        login(driver, user)
    assert not check_login_status(driver)
