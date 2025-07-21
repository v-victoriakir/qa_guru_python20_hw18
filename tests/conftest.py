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
    api.login_and_get_cookies()

    browser.open("/")
    for cookie in api.session.cookies:
        browser.driver.add_cookie({
            "name": cookie.name,
            "value": cookie.value,
            "domain": cookie.domain,
            "path": cookie.path
        })
    browser.open("/")

    ui = DemoWebShopUI()

    # A helper method inside fixture to add items before yielding
    def add_items_to_cart(items):
        # items: list of dicts like [{'item_id': 45, 'quantity': 5}, ...]
        for item in items:
            api.add_item_in_shopping_cart(item_id=item['item_id'], quantity=item['quantity'])

    # Attach this helper so tests can call if they want
    ui.api_add_items = add_items_to_cart

    yield ui, api

    ui.empty_cart()
