
import uuid


def generate_user_data():
    unique_id = uuid.uuid4().hex

    return {
        "email": f"test_{unique_id}@example.com",
        "password": "TestPassword123",
        "name": "Test User"
    }
