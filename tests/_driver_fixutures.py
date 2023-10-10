import pytest
from selenium import webdriver

from pyjpboatrace.drivers import (
    HTTPGetDriver,
    create_chrome_driver,
    create_firefox_driver,
    create_edge_driver,
    create_httpget_driver,
)


@pytest.fixture(scope="session")
def chrome_driver() -> webdriver.Chrome:
    d = None
    try:
        d = create_chrome_driver()
        yield d
    finally:
        if d is not None:
            d.close()


@pytest.fixture(scope="session")
def firefox_driver() -> webdriver.Firefox:
    d = None
    try:
        d = create_firefox_driver()
        yield d
    finally:
        if d is not None:
            d.close()


@pytest.fixture(scope="session")
def edge_driver() -> webdriver.Edge:
    d = None
    try:
        d = create_edge_driver()
        yield d
    finally:
        if d is not None:
            d.close()


@pytest.fixture(scope="session")
def httpget_driver() -> HTTPGetDriver:
    d = None
    try:
        d = create_httpget_driver()
        yield d
    finally:
        if d is not None:
            d.close()


@pytest.fixture(
    scope="session",
    params=[
        create_firefox_driver,
        create_chrome_driver,
        # create_edge_driver,  # TODO
    ]
)
def driver_not_http_get_driver(request):
    driver = None
    try:
        driver = request.param()
        yield driver
    finally:
        if driver is not None:
            driver.close()


@pytest.fixture(
    scope="session",
    params=[
        create_firefox_driver,
        create_chrome_driver,
        # create_edge_driver,  # TODO
        create_httpget_driver,
    ]
)
def driver(request):
    driver = None
    try:
        driver = request.param()
        yield driver
    finally:
        if driver is not None:
            driver.close()
