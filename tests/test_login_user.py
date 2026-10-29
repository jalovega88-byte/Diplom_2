
import allure
import pytest
import requests

from urls import LOGIN_USER_URL


@allure.feature("Авторизация пользователя")
class TestLoginUser:

    @allure.title("Успешный вход существующего пользователя")
    def test_login_existing_user(self, created_user):
        response = requests.post(
            LOGIN_USER_URL,
            json={
                "email": created_user["email"],
                "password": created_user["password"]
            },
            timeout=10
        )

        response_data = response.json()

        assert response.status_code == 200
        assert response_data["success"] is True
        assert "accessToken" in response_data
        assert "refreshToken" in response_data

    @allure.title("Вход с неверными данными: {invalid_field}")
    @pytest.mark.parametrize(
        "invalid_field",
        ["email", "password"]
    )
    def test_login_with_invalid_credentials(
        self, created_user, invalid_field
    ):
        login_data = {
            "email": created_user["email"],
            "password": created_user["password"]
        }

        if invalid_field == "email":
            login_data["email"] = "wrong_" + created_user["email"]
        else:
            login_data["password"] = "WrongPassword123"

        response = requests.post(
            LOGIN_USER_URL,
            json=login_data,
            timeout=10
        )

        assert response.status_code == 401
        assert response.json()["success"] is False
