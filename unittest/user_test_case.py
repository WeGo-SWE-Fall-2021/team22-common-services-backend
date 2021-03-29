import unittest
import sys
sys.path.insert(1, "../")
from User import User


class UserTestCase(unittest.TestCase):

    def test_user_creation(self):
        data = {
            "fname": "firstname",
            "lname": "lastname",
            "phoneNumber": "11111",
            "email": "email@email.com",
            "username": "user",
            "password": "pwdtest"
        }
        user = User(data)
        self.assertIsNotNone(user)

    def test_user_data_equals(self):
        data = {
            "fname": "firstname",
            "lname": "lastname",
            "phoneNumber": "11111",
            "email": "email@email.com",
            "username": "user",
            "password": "pwdtest"
        }
        user = User(data)
        self.assertIsNotNone(user)
        self.assertEqual(user.fname, "firstname")
        self.assertEqual(user.lname, "lastname")
        self.assertEqual(user.phoneNumber, "11111")
        self.assertEqual(user.email, "email@email.com")
        self.assertEqual(user.username, "user")
        self.assertEqual(user.password, "pwdtest")

    def test_user_data_change(self):
        data = {
            "fname": "firstname",
            "lname": "lastname",
            "phoneNumber": "11111",
            "email": "email@email.com",
            "username": "user",
            "password": "pwdtest"
        }
        user = User(data)
        user.username = "new_username"
        self.assertEqual(user.username, "new_username")
        user.password = "new_pwdtest"
        self.assertEqual(user.password, "new_pwdtest")
        user.email = "new@new.com"
        self.assertEqual(user.email, "new@new.com")
        user.fname = "newfirstname"
        self.assertEqual(user.fname, "newfirstname")
        user.lname = "newlastname"
        self.assertEqual(user.lname, "newlastname")
        user.phoneNumber = "00000"
        self.assertEqual(user.phoneNumber, "00000")


if __name__ == '__main__':
    unittest.main()
