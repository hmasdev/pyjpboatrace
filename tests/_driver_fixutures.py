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
    d = create_chrome_driver()
    yield d
    d.close()


@pytest.fixture(scope="session")
def firefox_driver() -> webdriver.Firefox:
    d = create_firefox_driver()
    yield d
    d.close()


@pytest.fixture(scope="session")
def edge_driver() -> webdriver.Edge:
    d = create_edge_driver()
    yield d
    d.close()


@pytest.fixture(scope="session")
def httpget_driver() -> HTTPGetDriver:
    d = create_httpget_driver()
    yield d
    d.close()
