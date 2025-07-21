import os

import allure
import requests
from dotenv import load_dotenv
from helpers.logger import response_logging, response_attaching

load_dotenv()


class DemoWebShopApi:
    BASE_URL = "https://demowebshop.tricentis.com"

    def __init__(self):
        self.session = requests.Session()
        self.email = os.getenv("DEMOWEBSHOP_EMAIL")
        self.password = os.getenv("DEMOWEBSHOP_PASSWORD")

    @allure.step("Авторизация пользователя через API")
    def login_and_get_cookies(self):
        response = self.session.post(
            url=f"{self.BASE_URL}/login",
            data={"Email": self.email, "Password": self.password, "RememberMe": False},
            allow_redirects=False
        )
        assert response.status_code == 302, (
            f"Login failed: expected 302 redirect, got {response.status_code}\n"
            f"Response text: {response.text}"
        )

        # Add logging and Allure attachments
        response_logging(response)
        response_attaching(response)

        auth_cookie = response.cookies.get("NOPCOMMERCE.AUTH")
        assert auth_cookie is not None, "Login succeeded but no 'NOPCOMMERCE.AUTH' cookie was found."

        self.session.cookies.set(
            "NOPCOMMERCE.AUTH",
            auth_cookie,
            domain="demowebshop.tricentis.com"
        )
        return auth_cookie

    @allure.step("Добавление товара в корзину")
    def add_item_in_shopping_cart(self, item_id: int, quantity: int = 1):
        product_url = f"{self.BASE_URL}/addproducttocart/catalog/{item_id}/1/{quantity}"
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

        # Add logging and Allure attachments
        response_logging(response)
        response_attaching(response)

        assert response.status_code == 200, f"Failed to add item to cart: {response.status_code}, {response.text}"
        return response
