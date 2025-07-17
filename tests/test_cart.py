import allure

from api.api_methods import DemoWebShopApi
from ui.ui_methods import DemoWebShopUI


@allure.title("Добавление одного товара в корзину")
def test_to_add_single_item_in_cart():
    api = DemoWebShopApi()
    ui = DemoWebShopUI()

    api.add_item_in_shopping_cart(item_id=45, quantity=1)
    ui.cart_page_open()
    ui.check_item_is_added_to_cart(item_name='Fiction')


@allure.title("Добавление нескольких товаров в корзину")
def test_to_add_different_items_in_cart():
    api = DemoWebShopApi()
    ui = DemoWebShopUI()

    api.add_item_in_shopping_cart(item_id=45, quantity=5)
    api.add_item_in_shopping_cart(item_id=80, quantity=3)
    ui.cart_page_open()
    ui.check_added_item_quantity(item_name='Fiction', quantity=5)
    ui.check_added_item_quantity(item_name='Phone Cover', quantity=3)
