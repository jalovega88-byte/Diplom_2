
import allure
import pytest
import requests

from helpers import generate_user_data
from urls import CREATE_USER_URL, DELETE_USER_URL


@allure.feature("Создание пользователя")
class TestCreateUser:

    @allure.title("Успешная регистрация уникального пользователя")
    def test_create_unique_user(self):
        user_data = generate_user_data()

        response = requests.post(
            CREATE_USER_URL,
            json=user_data,
            timeout=10
        )

        response_data = response.json()

        try:
            assert response.status_code == 200
            assert response_data["success"] is True
            assert "accessToken" in response_data
            assert "refreshToken" in response_data
        finally:
            token = response_data.get("accessToken")

            if token:
                delete_response = requests.delete(
                    DELETE_USER_URL,
                    headers={"Authorization": token},
                    timeout=10
                )

                assert delete_response.status_code == 202, (
                    f"Не удалось удалить пользователя: "
                    f"{delete_response.status_code}, "
                    f"{delete_response.text}"
                )

    @allure.title("Нельзя зарегистрировать пользователя повторно")
    def test_create_existing_user(self, created_user):
        response = requests.post(
            CREATE_USER_URL,
            json=created_user,
            timeout=10
        )

        assert response.status_code == 403
        assert response.json()["success"] is False

    @allure.title("Регистрация без обязательного поля: {missing_field}")
    @pytest.mark.parametrize(
        "missing_field",
        ["email", "password", "name"]
    )
    def test_create_user_without_required_field(self, missing_field):
        user_data = generate_user_data()
        user_data.pop(missing_field)

        response = requests.post(
            CREATE_USER_URL,
            json=user_data,
            timeout=10
        )

        assert response.status_code == 403
        assert response.json()["success"] is False
