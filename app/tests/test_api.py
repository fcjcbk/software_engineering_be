from fastapi.testclient import TestClient
from app.main import app
from app.db import user
from app import secure
from app.logger import get_logger

client = TestClient(app)
logger = get_logger(__name__)

def test_get_user_by_id():
    response_json = client.post("/api/v1/login", json={"account": "123", "password": "123"}).json()
    token = response_json['access_token']

    response = client.get("/api/v1/user/123", headers={"Authorization": f"Bearer {token}"})
    # Assume
    expected_user = user.UserModel(
            userid=123,
            username="student",
            password=secure.get_password_hash("123"),
            email="123@qq.com",
            major="string",
            role=0,
            telephone="string"
        )
    logger.info(response.json())
    assert secure.verify_password("123", response.json()['password']) == True
    assert response.status_code == 200
    # assert response.json() == expected_user
