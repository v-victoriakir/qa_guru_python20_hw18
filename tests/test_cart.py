import allure

from api.api_methods import DemoWebShopApi
from ui.ui_methods import DemoWebShopUI

@allure.epic("demowebshop")
@allure.feature("Корзина")
@allure.story("Добавление товаров в корзину")

@allure.title("Добавление одного товара в корзину")
def test_to_add_single_item_in_cart(authorized_user):
    api = DemoWebShopApi()
    ui = DemoWebShopUI()

    api.login_and_get_cookies()
    api.add_item_in_shopping_cart(item_id=45)
    ui.cart_page_open()
    ui.check_item_is_added_to_cart('Fiction')


@allure.title("Добавление нескольких товаров одного типа в корзину")
def test_to_add_different_items_in_cart(authorized_user):
    api = DemoWebShopApi()
    ui = DemoWebShopUI()

    api.login_and_get_cookies()
    api.add_item_in_shopping_cart(item_id=45, quantity=5)
    ui.cart_page_open()
    ui.check_added_item_quantity(item_name='Fiction', quantity=5)


@allure.title("Добавление нескольких товаров в разном количестве в корзину")
def test_to_add_multiple_items(authorized_user):
    ui, api = authorized_user

    # Add items using the helper attached to UI object
    ui.api_add_items([
        {'item_id': 45, 'quantity': 5},
        {'item_id': 36, 'quantity': 3},
    ])
    ui.cart_page_open()
    ui.check_added_item_quantity(item_name='Fiction', quantity=5)
    ui.check_added_item_quantity(item_name='Blue Jeans', quantity=3)
