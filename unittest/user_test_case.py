import unittest
import sys
import xmlrunner

sys.path.insert(1, "../")
from user import User


class UserTestCase(unittest.TestCase):

    def test_user_creation(self):
        data = {
            "_id": "1515646454",
            "firstName": "firstname",
            "lastName": "lastname",
            "phoneNumber": "11111",
            "email": "email@email.com",
            "username": "user",
            "password": "pwdtest"
        }
        user = User(data)
        self.assertIsNotNone(user)

    def test_user_data_equals(self):
        data = {
            "_id": "1515646454",
            "firstName": "firstname",
            "lastName": "lastname",
            "phoneNumber": "11111",
            "email": "email@email.com",
            "username": "user",
            "password": "pwdtest"
        }
        user = User(data)
        self.assertIsNotNone(user)
        self.assertEqual(user.id, "1515646454")
        self.assertEqual(user.firstName, "firstname")
        self.assertEqual(user.lastName, "lastname")
        self.assertEqual(user.phoneNumber, "11111")
        self.assertEqual(user.email, "email@email.com")
        self.assertEqual(user.username, "user")
        self.assertEqual(user.password, "pwdtest")

    def test_user_data_change(self):
        data = {
            "_id": "1515646454",
            "firstName": "firstname",
            "lastName": "lastname",
            "phoneNumber": "11111",
            "email": "email@email.com",
            "username": "user",
            "password": "pwdtest"
        }
        user = User(data)
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
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))