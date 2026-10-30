
import pytest
import requests

from helpers import generate_user_data
from urls import CREATE_USER_URL, DELETE_USER_URL


@pytest.fixture
def created_user():
    user_data = generate_user_data()

    response = requests.post(
        CREATE_USER_URL,
        json=user_data,
        timeout=10
    )

    assert response.status_code == 200, (
        f"Не удалось создать пользователя: {response.text}"
    )

    token = response.json()["accessToken"]

    try:
        yield user_data
    finally:
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


@pytest.fixture
def user_for_registration():
    user_data = generate_user_data()
    user = {"data": user_data, "token": None}

    yield user

    if user["token"]:
        delete_response = requests.delete(
            DELETE_USER_URL,
            headers={"Authorization": user["token"]},
            timeout=10
        )

        assert delete_response.status_code == 202, (
            f"Не удалось удалить пользователя: "
            f"{delete_response.status_code}, "
            f"{delete_response.text}"
        )
