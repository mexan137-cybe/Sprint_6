import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from utils.failure_artifacts import save_failure_artifacts
WINDOW_SIZE = (1440, 900)


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="firefox",
        choices=["firefox", "chrome"],
        help="Браузер, в котором запускать тесты: firefox (по умолчанию) или chrome",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Запустить браузер в headless-режиме",
    )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


def _build_firefox_driver(headless: bool):
    options = FirefoxOptions()
    if headless:
        options.add_argument("--headless")
    service = FirefoxService(GeckoDriverManager().install())
    return webdriver.Firefox(service=service, options=options)


def _build_chrome_driver(headless: bool):
    options = ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    service = ChromeService(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")

    if browser == "chrome":
        drv = _build_chrome_driver(headless)
    else:
        drv = _build_firefox_driver(headless)

    drv.set_window_size(*WINDOW_SIZE)

    yield drv

    test_failed = any(
        getattr(request.node, f"rep_{when}", None) is not None
        and getattr(request.node, f"rep_{when}").failed
        for when in ("setup", "call")
    )

    if test_failed:
        save_failure_artifacts(drv, request.node.name)

    drv.quit()

