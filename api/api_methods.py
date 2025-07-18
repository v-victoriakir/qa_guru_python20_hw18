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
        assert response.status_code == 302, (
            f"Login failed: expected 302 redirect, got {response.status_code}\n"
            f"Response text: {response.text}"
        )
        auth_cookie = response.cookies.get("NOPCOMMERCE.AUTH")
        assert auth_cookie is not None, "Login succeeded but no 'NOPCOMMERCE.AUTH' cookie was found."

        self.session.cookies.set("NOPCOMMERCE.AUTH", auth_cookie, domain="demowebshop.tricentis.com")
        return auth_cookie

    @allure.step("Добавление товара в корзину")
    def add_item_in_shopping_cart(self, item_id, quantity=1):
        product_url = self.base_url + f"/addproducttocart/details/{item_id}/1"
        data = {f"addtocart_{item_id}.EnteredQuantity": str(quantity)}

        response = self.session.post(
            url=product_url,
            data=data,
            allow_redirects=False,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "X-Requested-With": "XMLHttpRequest"
            }
        )

        assert response.status_code == 200, f"Failed to add item to cart: {response.status_code}, {response.text}"
        return response
