import allure

from selene import browser, have

BASE_URL = "https://demowebshop.tricentis.com"


class DemoWebShopUI:
    def __init__(self):
        self.cart_url = BASE_URL + "/cart"

    @allure.step("Открыта страница корзины")
    def cart_page_open(self):
        browser.open(self.cart_url)

    @allure.step("В корзину добавлен продукт {item_name}")
    def check_item_is_added_to_cart(self, item_name):
        browser.element('.cart-item-row').should(have.text(item_name))

    @allure.step("В корзину добавлен продукт {item_name} в количестве {quantity}")
    def check_added_item_quantity(self, item_name, quantity):
        browser.element('.cart-item-row').should(have.text(item_name))
        browser.element('.qty-input').should(have.value(str(quantity)))
