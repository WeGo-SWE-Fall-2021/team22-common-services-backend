import unittest
import sys
import time
import requests
import xmlrunner

from threading import Thread

sys.path.insert(1, "../")
from http.server import HTTPServer
from server import SimpleHTTPRequestHandler

# Global variables used in the unittest

port = 4003

user_data_payload = {
    "_id": "1515646454",
    "firstName": "test_firstName",
    "lastName": "test_lastName",
    "phoneNumber": "test_phoneNumber",
    "email": "test@test.com",
    "username": "test_username",
    "password": "test_password"
}

# This is a demo that unittests the python endpoints. Beware, order matters in this case since we are
# dealing witht the database, might vary depending on how you're tesing

# TEST METHOD ORDER STRUCTURE $
# def test_(number here)_(subject here):


class ServerTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up server
        cls._server = HTTPServer(('', port), SimpleHTTPRequestHandler)
        cls._server_thread = Thread(None, cls._server.serve_forever)
        cls._server_thread.start()

    ############## DEMAND SIDE ##############

    def test_demand_1_register_user_valid_request(self):
        register_payload = user_data_payload.copy()
        register_payload["cloud"] = "demand"
        response = requests.post(f"http://localhost:{port}/register", json=register_payload, timeout=5)
        self.assertEqual(response.status_code, 201)
        response.close()

    def test_demand_2_register_user_already_registered_request(self):
        register_payload = user_data_payload.copy()
        register_payload["cloud"] = "demand"
        response = requests.post(f"http://localhost:{port}/register", json=register_payload, timeout=5)
        self.assertEqual(response.status_code, 401)
        response.close()

    def test_demand_3_login_user_credentials_valid_request(self):
        login_payload = {
            "cloud": "demand",
            "username": user_data_payload["username"],
            "password": user_data_payload["password"],
        }
        response = requests.post(f"http://localhost:{port}/login", json=login_payload, timeout=5)
        self.assertEqual(response.status_code, 200)
        response.close()

    def test_demand_4_login_user_credentials_invalid_request(self):
        login_payload = {
            "cloud": "demand",
            "username": "hahaha",
            "password": "goburrrrr",
        }
        response = requests.post(f"http://localhost:{port}/login", json=login_payload, timeout=5)
        self.assertEqual(response.status_code, 401)
        response.close()

    ############## SUPPLY SIDE ##############

    def test_supply_1_register_user_valid_request(self):
        register_payload = user_data_payload.copy()
        register_payload["cloud"] = "supply"
        response = requests.post(f"http://localhost:{port}/register", json=register_payload, timeout=5)
        self.assertEqual(response.status_code, 201)
        response.close()

    def test_supply_2_register_user_already_registered_request(self):
        register_payload = user_data_payload.copy()
        register_payload["cloud"] = "supply"
        response = requests.post(f"http://localhost:{port}/register", json=register_payload, timeout=5)
        self.assertEqual(response.status_code, 401)
        response.close()

    def test_supply_3_login_user_credentials_valid_request(self):
        login_payload = {
            "cloud": "supply",
            "username": user_data_payload["username"],
            "password": user_data_payload["password"],
        }
        response = requests.post(f"http://localhost:{port}/login", json=login_payload, timeout=5)
        self.assertEqual(response.status_code, 200)
        response.close()

    def test_supply_4_login_user_credentials_invalid_request(self):
        login_payload = {
            "cloud": "supply",
            "username": "hahaha",
            "password": "goburrrrr",
        }
        response = requests.post(f"http://localhost:{port}/login", json=login_payload, timeout=5)
        self.assertEqual(response.status_code, 401)
        response.close()

    @classmethod
    def tearDownClass(cls):
        # tear down server
        cls._server.shutdown()
        cls._server_thread.join()

if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))