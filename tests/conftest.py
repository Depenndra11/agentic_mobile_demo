import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from config.settings import Settings


def get_driver():
    """
    Create Chrome driver in mobile emulation mode.
    """

    options = Options()

    options.add_experimental_option(
        "mobileEmulation",
        {
            "deviceName": Settings.DEVICE
        }
    )

    options.add_argument("--disable-notifications")

    driver = webdriver.Chrome(options=options)

    driver.get(Settings.BASE_URL)

    return driver


@pytest.fixture(scope="session")
def driver():

    driver = get_driver()

    yield driver

    driver.quit()