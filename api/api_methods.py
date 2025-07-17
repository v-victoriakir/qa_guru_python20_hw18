import os

import allure
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://demowebshop.tricentis.com"


class DemoWebShopApi:
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.email = os.getenv("DEMOWEBSHOP_EMAIL")
        self.password = os.getenv("DEMOWEBSHOP_PASSWORD")

    @allure.step("Авторизация пользователя через API")
    def login_and_get_cookies(self):
        response = self.session.post(
            url=self.base_url + "/login",
            data={"Email": self.email, "Password": self.password, "RememberMe": False},
            allow_redirects=False
        )
        cookies = response.cookies.get("NOPCOMMERCE.AUTH")
        return cookies

    @allure.step("Добавление товара в корзину")
    def add_item_in_shopping_cart(self, item_id, quantity):
        response = self.session.post(
            url=self.base_url + f"addproducttocart/details/{item_id}/1",
            data={f'addtocart_{item_id}.EnteredQuantity': {quantity}},
            allow_redirects=False
        )
        return response
