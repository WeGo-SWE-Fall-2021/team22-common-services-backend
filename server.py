import json
import bcrypt
import hashlib
from random import getrandbits
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from MongoUtils import initMongoFromCloud
from User import User


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    version = '0.0.1'

    # Reads the POST data from the HTTP header
    def extract_POST_Body(self):
        postBodyLength = int(self.headers['content-length'])
        postBodyString = self.rfile.read(postBodyLength)
        postBodyDict = json.loads(postBodyString)
        return postBodyDict

    # handle post requests
    def do_POST(self):
        status = 404  # HTTP Request: Not found
        postData = self.extract_POST_Body()  # store POST data into a dictionary
        path = self.path
        cloud = postData['cloud']
        client = initMongoFromCloud(cloud)
        db = client['team22_' + cloud]
        responseBody = {
            'status': 'failed',
            'message': 'Request not found'
        }

        # receiving registration requests and writing their data to the database
        if '/register' in path:
            status = 401
            responseBody = {
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
                responseBody = {
                    'status': 'success',
                    'message': 'Successfully registered user.'
                }
        elif '/login' in path:
            status = 401
            responseBody = {
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
                    responseBody = {
                        'status': 'success',
                        'message': 'Successfully logged in.'
                    }
                    self.send_header("Set-Cookie", "token=" + token)

        self.send_response(status)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        responseString = json.dumps(responseBody).encode()
        self.wfile.write(responseString)
        client.close()

    def do_GET(self):
        return


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
