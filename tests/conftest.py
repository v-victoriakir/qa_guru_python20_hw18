import pytest
from selene import browser

from api.api_methods import DemoWebShopApi
from ui.ui_methods import DemoWebShopUI
from utils import attach

BASE_URL = "https://demowebshop.tricentis.com"


@pytest.fixture(scope="function", autouse=True)
def browser_config():
    browser.config.base_url = BASE_URL
    browser.config.window_height = 1080
    browser.config.window_width = 1920

    yield

    attach.add_html(browser)
    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_video(browser)

    browser.quit()


@pytest.fixture(scope="function")
def authorized_user(browser_config):
    api = DemoWebShopApi()
    auth_cookies = api.login_and_get_cookies()

    # Open any page to set cookies into browser context
    browser.open("/")
    browser.driver.add_cookie({
        "name": "NOPCOMMERCE.AUTH",
        "value": auth_cookies,
        "domain": "demowebshop.tricentis.com",
        "path": "/"
    })

    # # Reload with cookies set
    browser.open("/")

    yield  # Test runs here

    # open cart to empty it after each test
    ui = DemoWebShopUI()
    ui.cart_page_open()
    ui.empty_cart()
