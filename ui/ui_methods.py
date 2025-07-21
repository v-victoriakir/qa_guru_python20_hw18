import allure

from selene import browser, have, be


class DemoWebShopUI:
    @allure.step("Открыта страница корзины")
    def cart_page_open(self):
        browser.open("/cart")

    @allure.step("В корзину добавлен продукт {item_name}")
    def check_item_is_added_to_cart(self, item_name):
        browser.element('.cart-item-row').should(have.text(item_name))

    @allure.step("В корзину добавлен продукт {item_name} в количестве {quantity}")
    def check_added_item_quantity(self, item_name, quantity):
        row = browser.all('.cart-item-row').element_by(have.text(item_name))
        row.element('.qty-input').should(have.value(str(quantity)))

    @allure.step("Корзина очищена")
    def empty_cart(self):
        self.cart_page_open()
        for element in browser.all('input[name=removefromcart]'):
            element.should(be.clickable).click()
        browser.element('input[name=updatecart]').click()
        browser.element(".order-summary-content").should(have.text("Your Shopping Cart is empty!"))
