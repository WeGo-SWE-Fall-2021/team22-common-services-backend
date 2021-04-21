import unittest
import sys

sys.path.insert(1, "../")
from user import User

user_data_1 = {
    "_id": "1515646454",
    "firstName": "firstname",
    "lastName": "lastname",
    "phoneNumber": "11111",
    "email": "email@email.com",
    "username": "user",
    "password": "pwdtest"
}

class UserTestCase(unittest.TestCase):

    def test_user_creation(self):
        user = User(user_data_1)
        self.assertIsNotNone(user)

    def test_user_data_equals(self):
        user = User(user_data_1)
        self.assertIsNotNone(user)
        self.assertEqual(user.id, user_data_1["_id"])
        self.assertEqual(user.firstName, user_data_1["firstName"])
        self.assertEqual(user.lastName, user_data_1["lastName"])
        self.assertEqual(user.phoneNumber, user_data_1["phoneNumber"])
        self.assertEqual(user.email, user_data_1["email"])
        self.assertEqual(user.username, user_data_1["username"])
        self.assertEqual(user.password, user_data_1["password"])

    def test_user_data_change(self):
        user = User(user_data_1)
        with self.assertRaises(AttributeError):
            user.id = "new_id"
        user.username = "new_username"
        self.assertEqual(user.username, "new_username")
        user.password = "new_pwdtest"
        self.assertEqual(user.password, "new_pwdtest")
        user.email = "new@new.com"
        self.assertEqual(user.email, "new@new.com")
        user.firstName = "newfirstname"
        self.assertEqual(user.firstName, "newfirstname")
        user.lastName = "newlastname"
        self.assertEqual(user.lastName, "newlastname")
        user.phoneNumber = "00000"
        self.assertEqual(user.phoneNumber, "00000")


if __name__ == '__main__':
    unittest.main()