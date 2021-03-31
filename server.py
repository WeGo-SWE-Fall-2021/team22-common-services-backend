import datetime
import json
import bcrypt
import hashlib
import urllib.parse as urlparse
from urllib.parse import parse_qs
from random import getrandbits
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from MongoUtils import initMongoFromCloud
from User import User


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    version = '0.1.0'

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

            # TODO: add email address soon, but as of now username is fine
            user = User(postData)
            registeredUsernameCount = db.user.count_documents({"username": user.username})
            if registeredUsernameCount == 0:
                # hash and salt password
                password = user.password.encode()
                salt = bcrypt.gensalt()
                hashed = bcrypt.hashpw(password, salt)
                user.password = hashed

                # generate secure token
                ip = self.client_address[0].encode()
                username = user.username.encode()
                random = str(getrandbits(256)).encode()
                token = hashlib.sha256(username + ip + random).hexdigest()

                # Insert data to database
                db.user.insert_one({
                    "fname": user.fname,
                    "lname": user.lname,
                    "phoneNumber": user.phoneNumber,
                    "email": user.email,
                    "username": user.username,
                    "password": user.password,
                    "token": token
                })

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

            data = db.user.find_one({"username": postData["username"]})
            if data is not None:
                user = User(data)
                password = postData["password"].encode()
                # check password that was on database with the provided password
                matched = bcrypt.checkpw(password, user.password)
                if matched:
                    status = 200
                    token = db.user.find_one({"username": user.username})["token"]
                    response = {
                        'status': 'success',
                        'message': 'Successfully logged in.'
                    }
                    url = cloud + ".team22.sweispring21.tk"
                    headers["Set-Cookie"] = "token=" + token + "; Domain=" + url + "; Secure; HttpOnly"

        elif '/logout' in path:
            url = cloud + ".team22.sweispring21.tk"
            time_format = "%a, %d %b %Y %H:%M:%S %Z"
            expires = "%s" % ((datetime.datetime.now() + datetime.timedelta(-1)).strftime(time_format)) + "GMT"
            print(expires)
            headers["Set-Cookie"] = "token=; Domain=" + url + "; Secure; HttpOnly; Expire=" + expires + ";"
            status = 200
            response = {
                'status': 'success',
                'message': 'Successfully logged out.'
            }

        self.writeRequest(status, headers, response)
        client.close()

    # This handles any GET requests
    def do_GET(self):
        path = self.path
        status = 401
        get_data = dict(urlparse.parse_qsl(urlparse.urlsplit(path).query))
        cloud = get_data["cloud"]
        headers = {}
        response = {}
        client = initMongoFromCloud(cloud)
        db = client['team22_' + cloud]
        if '/user' in path:
            tokenStr = self.headers["Cookie"]
            if tokenStr is not None:
                token = tokenStr.split('=')[1]
                user = db.user.find_one({"token": token})
                if user is not None:
                    user = User(user)
                    # TODO add extra attributes based on cloud config
                    status = 200
                    response = {
                        "fname": user.fname,
                        "lname": user.lname,
                        "email": user.email,
                        "username": user.username
                    }

        self.writeRequest(status, headers, response)
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
