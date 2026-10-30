
import allure
import requests

from urls import CREATE_ORDER_URL, INGREDIENTS_URL, LOGIN_USER_URL


@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа без авторизации с ингредиентами")
    def test_create_order_without_authorization(self):
        ingredients_response = requests.get(
            INGREDIENTS_URL,
            timeout=10
        )

        assert ingredients_response.status_code == 200

        ingredients = ingredients_response.json()["data"]
        ingredient_id = ingredients[0]["_id"]

        response = requests.post(
            CREATE_ORDER_URL,
            json={"ingredients": [ingredient_id]},
            timeout=10
        )

        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_with_authorization(self, created_user):
        login_response = requests.post(
            LOGIN_USER_URL,
            json={
                "email": created_user["email"],
                "password": created_user["password"]
            },
            timeout=10
        )

        assert login_response.status_code == 200
        token = login_response.json()["accessToken"]

        ingredients_response = requests.get(
            INGREDIENTS_URL,
            timeout=10
        )

        assert ingredients_response.status_code == 200
        ingredient_id = ingredients_response.json()["data"][0]["_id"]

        response = requests.post(
            CREATE_ORDER_URL,
            json={"ingredients": [ingredient_id]},
            headers={"Authorization": token},
            timeout=10
        )

        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title("Нельзя создать заказ без ингредиентов")
    def test_create_order_without_ingredients(self):
        response = requests.post(
            CREATE_ORDER_URL,
            json={"ingredients": []},
            timeout=10
        )

        assert response.status_code == 400
        assert response.json()["success"] is False

    @allure.title("Нельзя создать заказ с неверным хешем ингредиента")
    def test_create_order_with_invalid_ingredient_hash(self):
        response = requests.post(
            CREATE_ORDER_URL,
            json={"ingredients": ["invalid_ingredient_hash"]},
            timeout=10
        )

        assert response.status_code == 500
