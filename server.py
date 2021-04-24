import datetime
import json
import bcrypt
import hashlib
import urllib.parse as urlparse
import jwt
import os

from urllib.parse import parse_qs
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from utils.mongoutils import initMongoFromCloud
from uuid import uuid4
from user import User
from dotenv import load_dotenv

load_dotenv()


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    version = '0.1.1'

    def writeRequest(self, status, headers, response):
        self.send_response(status)
        # Send headers from dictionary
        for key in headers:
            self.send_header(key, headers[key])
        self.end_headers()
        responseString = json.dumps(response).encode()
        self.wfile.write(responseString)

    # Reads the POST data from the HTTP header
    def extract_POST_Body(self):
        postBodyLength = int(self.headers['content-length'])
        postBodyString = self.rfile.read(postBodyLength)
        postBodyDict = json.loads(postBodyString)
        return postBodyDict

    # handle post requests
    def do_POST(self):
        path = self.path
        status = 404  # HTTP Request: Not found
        postData = self.extract_POST_Body()  # store POST data into a dictionary
        cloud = postData['cloud']
        client = initMongoFromCloud(cloud)
        db = client['team22_' + cloud]
        collection = db.Customer if cloud == "demand" else db.FleetManager
        headers = {
            "Content-Type": "application/json"
        }
        response = {
            'status': 'failed',
            'message': 'Request not found'
        }

        # receiving registration requests and writing their data to the database
        if '/register' in path:
            status = 401
            response = {
                'status': 'failed',
                'message': 'There is already a user registered with that username'  # TODO: Distinguish similarities
            }

            user = User(postData)
            registeredUsernameCount = collection.count_documents({"username": user.username.lower()})
            registeredEmailCount = collection.count_documents({"email": user.email.lower()})

            if registeredUsernameCount == 0 and registeredEmailCount == 0:
                # hash and salt password
                password = user.password.encode()
                salt = bcrypt.gensalt()
                hashed = bcrypt.hashpw(password, salt)
                user.password = hashed

                extraData = {}
                # Extra attributes for FleetManager if it's coming from supply cloud
                if (cloud == "supply"):
                    extraData["dockAddress"] = ""
                    extraData["dockNumber"] = ""
                    extraData["fleetIds"] = []

                # Common Data for FleetManager and Customer Database
                data = {
                        "_id": user.id,
                        "firstName": user.firstName,
                        "lastName": user.lastName,
                        "phoneNumber": user.phoneNumber,
                        "email": user.email.lower(),
                        "username": user.username.lower(),
                        "password": user.password
                }

                # Specifically for FleetManager if it needs extra attributes
                data.update(extraData)

                # Insert data to database
                collection.insert_one(data)

                status = 201  # HTTP Request: Created, Only if the user was registered
                response = {
                    'status': 'success',
                    'message': 'Successfully registered user.'
                }
        elif '/login' in path:
            status = 401
            response = {
                'status': 'failed',
                'message': 'Failed to find user with provided information'
            }

            data = collection.find_one({"username": postData["username"].lower()})
            if data is not None:
                user = User(data)
                password = postData["password"]
                # check password that was on database with the provided password
                matched = bcrypt.checkpw(password.encode('utf-8'), user.password)
                if matched:
                    status = 200
                    token_secret = os.getenv("TOKEN_SECRET")
                    token_payload = {
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
                        'iat': datetime.datetime.utcnow(),
                        'user_id': user.id
                    }
                    auth_token = jwt.encode(token_payload, token_secret, algorithm="HS256")
                    url = cloud + ".team22.sweispring21.tk"
                    headers["Set-Cookie"] = "token=" + auth_token + "; Domain=" + url + "; Path=/; Secure; HttpOnly"
                    response = {
                        'status': 'success',
                        'message': 'Successfully logged in.'
                    }

        elif '/logout' in path:
            url = cloud + ".team22.sweispring21.tk"
            time_format = "%a, %d %b %Y %H:%M:%S %Z"
            expires = "%s" % ((datetime.datetime.now() + datetime.timedelta(-1)).strftime(time_format)) + "GMT"
            headers["Set-Cookie"] = "token=; Domain=" + url + "; Path=/; Secure; HttpOnly; Expire=" + expires + ";"
            status = 200
            response = {
                'status': 'success',
                'message': 'Successfully logged out.'
            }

        client.close()
        self.writeRequest(status, headers, response)

    # This handles any GET requests
    def do_GET(self):
        path = self.path
        status = 401
        data_url = dict(urlparse.parse_qsl(urlparse.urlsplit(path).query))
        cloud = data_url["cloud"]
        client = initMongoFromCloud(cloud)
        db = client['team22_' + cloud]
        collection = db.Customer if cloud == "demand" else db.FleetManager
        headers = {}
        response_body = {}

        if '/user' in path:
            status = 401
            response_body = {
                "status": "failed",
                "message": "failed to retreive user: user not found"
            }

            tokenStr = self.headers["Cookie"]
            if tokenStr is not None:
                token = tokenStr.split('token=')[1].split(";")[0]
                try:
                    token_secret = os.getenv("TOKEN_SECRET")
                    token_decoded = jwt.decode(token, token_secret, algorithms="HS256")
                    user = collection.find_one({ "_id": token_decoded["user_id"]})
                    if user is not None:
                        user = User(user)
                        status = 200
                        response_body = {
                            "status": "success",
                            "message": "Successfully retreived user information",
                            "user": {
                                "firstName": user.firstName,
                                "lastName": user.lastName,
                                "email": user.email,
                                "username": user.username
                            }
                        }
                except:
                    response_body = {
                        "status": "failed",
                        "message": "failed to retreive user with token"
                    }
        self.writeRequest(status, headers, response_body)
        client.close()


def main():
    port = 4003  # Port 4001 reserved for demand backend
    server = HTTPServer(('', port), SimpleHTTPRequestHandler)
    print('Server is starting... Use <Ctrl+C> to cancel. Running on Port {}'.format(port))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Stopped server due to user interrupt")
    print("Server stopped")


if __name__ == "__main__":
    main()
