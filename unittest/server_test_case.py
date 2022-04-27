import unittest
import sys
import time
import requests
import json

sys.path.insert(1, sys.path[0] + "/../")

from threading import Thread
from utils.mongoutils import initMongo
from http.server import HTTPServer
from server import SimpleHTTPRequestHandler

# Global variables used in the unittest

port = 4003

user_data_one = {
    "_id": "1515646454",
    "firstName": "test_firstName",
    "lastName": "test_lastName",
    "phoneNumber": "test_phoneNumber",
    "email": "test@test.com",
    "username": "test_username",
    "password": "test_password"
}

demand_client = initMongo("demand")
supply_client = initMongo("supply")
demand_db = demand_client["team22_demand"]
supply_db = supply_client["team22_supply"]

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

        demand_db.Customer.delete_many({})
        supply_db.FleetManager.delete_many({})

        # this writes to the database with bcrypt so that we can test if our bcrypt passes
        payload_new_user = user_data_one.copy()
        payload_new_user["cloud"] = "demand"
        requests.post(f"http://localhost:{port}/register", json=payload_new_user, timeout=5)
        payload_new_user["cloud"] = "supply"
        requests.post(f"http://localhost:{port}/register", json=payload_new_user, timeout=5)

    ############## DEMAND SIDE ##############

    def test_demand_register_user_valid_request(self):
        payload_new_user = user_data_one.copy()
        payload_new_user["_id"] = "4164f6413"
        payload_new_user["cloud"] = "demand"
        payload_new_user["email"] = "ktor@kerg.com"
        payload_new_user["username"] = "uhhhhh"
        response = requests.post(f"http://localhost:{port}/register", json=payload_new_user, timeout=5)
        self.assertEqual(response.status_code, 201)
        response.close()

    def test_demand_register_user_already_registered_request(self):
        register_payload = user_data_one.copy()
        register_payload["cloud"] = "demand"
        response = requests.post(f"http://localhost:{port}/register", json=register_payload, timeout=5)
        self.assertEqual(response.status_code, 401)
        response.close()

    def test_demand_login_user_and_get_user_data(self):
        login_payload = {
            "cloud": "demand",
            "username": user_data_one["username"],
            "password": user_data_one["password"]
        }
        response = requests.post(f"http://localhost:{port}/login", json=login_payload, timeout=5)
        self.assertEqual(response.status_code, 200)
        response.close()
        token_str = response.headers["Set-Cookie"]
        self.assertIsNotNone(token_str)
        self.assertNotEqual(token_str, "")

        # Fetch user information
        cookies = { 
            "token": token_str.split("token=")[1].split(";")[0]
         }
        response_user = requests.get(f"http://localhost:{port}/user?cloud=demand", cookies=cookies, timeout=5)
        self.assertEqual(response_user.status_code, 200)
        response_user_json = json.loads(response_user.text)
        self.assertEqual(response_user_json["user"]["firstName"], user_data_one["firstName"])
        self.assertEqual(response_user_json["user"]["lastName"], user_data_one["lastName"])
        self.assertEqual(response_user_json["user"]["username"], user_data_one["username"])

    def test_demand_login_user_credentials_invalid_request(self):
        login_payload = {
            "cloud": "demand",
            "username": "hahaha",
            "password": "goburrrrr"
        }
        response = requests.post(f"http://localhost:{port}/login", json=login_payload, timeout=5)
        self.assertEqual(response.status_code, 401)
        response.close()

    def test_demand_fetch_user_token_empty(self):
        cookies = { 
            "token": ""
         }
        response_user = requests.get(f"http://localhost:{port}/user?cloud=demand", cookies=cookies, timeout=5)
        self.assertEqual(response_user.status_code, 401)

    def test_demand_fetch_user_token_invalid(self):
        cookies = { 
            "token": "ijwof4jfi4300"
         }
        response_user = requests.get(f"http://localhost:{port}/user?cloud=demand", cookies=cookies, timeout=5)
        self.assertEqual(response_user.status_code, 401)

    ############## SUPPLY SIDE ##############

    def test_supply_register_user_valid_request(self):
        payload_new_user = user_data_one.copy()
        payload_new_user["_id"] = "41286324789216464"
        payload_new_user["cloud"] = "supply"
        payload_new_user["email"] = "ktor@kerg.com"
        payload_new_user["username"] = "uhhhhh"
        response = requests.post(f"http://localhost:{port}/register", json=payload_new_user, timeout=5)
        self.assertEqual(response.status_code, 201)
        response.close()

    def test_supply_register_user_already_registered_request(self):
        register_payload = user_data_one.copy()
        register_payload["cloud"] = "supply"
        response = requests.post(f"http://localhost:{port}/register", json=register_payload, timeout=5)
        self.assertEqual(response.status_code, 401)
        response.close()

    def test_supply_login_user_and_get_user_data(self):
        login_payload = {
            "cloud": "supply",
            "username": user_data_one["username"],
            "password": user_data_one["password"]
        }
        response = requests.post(f"http://localhost:{port}/login", json=login_payload, timeout=5)
        self.assertEqual(response.status_code, 200)
        response.close()
        token_str = response.headers["Set-Cookie"]
        self.assertIsNotNone(token_str)
        self.assertNotEqual(token_str, "")

        # Fetch user information
        cookies = { 
            "token": token_str.split("token=")[1].split(";")[0]
         }
        response_user = requests.get(f"http://localhost:{port}/user?cloud=supply", cookies=cookies, timeout=5)
        self.assertEqual(response_user.status_code, 200)
        response_user_json = json.loads(response_user.text)
        self.assertEqual(response_user_json["user"]["firstName"], user_data_one["firstName"])
        self.assertEqual(response_user_json["user"]["lastName"], user_data_one["lastName"])
        self.assertEqual(response_user_json["user"]["username"], user_data_one["username"])

    def test_supply_login_user_credentials_invalid_request(self):
        login_payload = {
            "cloud": "supply",
            "username": "hahaha",
            "password": "goburrrrr"
        }
        response = requests.post(f"http://localhost:{port}/login", json=login_payload, timeout=5)
        self.assertEqual(response.status_code, 401)
        response.close()

    def test_supply_fetch_user_token_invalid(self):
        cookies = { 
            "token": "ijwof4jfi4300"
         }
        response_user = requests.get(f"http://localhost:{port}/user?cloud=supply", cookies=cookies, timeout=5)
        self.assertEqual(response_user.status_code, 401)

    def test_supply_fetch_user_token_empty(self):
        cookies = { 
            "token": ""
         }
        response_user = requests.get(f"http://localhost:{port}/user?cloud=supply", cookies=cookies, timeout=5)
        self.assertEqual(response_user.status_code, 401)

    @classmethod
    def tearDownClass(cls):
        # tear down server
        cls._server.shutdown()
        cls._server_thread.join()
        demand_db.Customer.delete_many({})
        supply_db.FleetManager.delete_many({})
        demand_client.close()
        supply_client.close()

if __name__ == '__main__':
    unittest.main()