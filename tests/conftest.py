import json

import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from appium import webdriver as appium_driver
from appium.options.android import UiAutomator2Options


with open("config/config.json", "r") as file:
    config = json.load(file)


@pytest.fixture(scope="function")
def driver():

    if config["automation_type"].lower() == "web":

        browser = config["web"]["browser"]

        if browser.lower() == "chrome":

            options = Options()

            driver = webdriver.Chrome(options=options)

        else:
            raise Exception(f"Unsupported browser: {browser}")

        driver.maximize_window()
        driver.get(config["web"]["base_url"])

    elif config["automation_type"].lower() == "mobile":

        options = UiAutomator2Options()

        options.platform_name = config["mobile"]["platform_name"]
        options.device_name = config["mobile"]["device_name"]
        options.automation_name = config["mobile"]["automation_name"]
        options.app_package = config["mobile"]["app_package"]
        options.app_activity = config["mobile"]["app_activity"]

        driver = appium_driver.Remote(
            config["mobile"]["appium_server"],
            options=options
        )

    else:
        raise Exception(
            f"Unsupported automation type: {config['automation_type']}"
        )

    yield driver

    driver.quit()