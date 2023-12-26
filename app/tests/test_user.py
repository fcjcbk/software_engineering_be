import unittest
from app.db import user
from app import secure

class TestUser(unittest.TestCase):
    def test_get_user_by_id(self):
        # Assume

        test_id = 123
        expected_user = user.UserModel(
            userid=123,
            username="student",
            password=secure.get_password_hash("123"),
            email="123@qq.com",
            major="string",
            role=0,
            telephone="string"
        )

        store_user = user.get_User()
        # Act
        result = store_user.get_user_by_id(test_id)
        print(result)
        print(expected_user)
        # Assert
        self.assertEqual(result, expected_user)

if __name__ == "__main__":
    unittest.main()
