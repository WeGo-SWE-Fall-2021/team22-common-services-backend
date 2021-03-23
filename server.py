import json
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
            # TODO: add email address soon, but as of now username is fine
            registeredUsernameCount = db.user.count_documents({"username": postData["username"]})
            if registeredUsernameCount == 0:
                # Convert user objet to JSON and add it to mongo
                user = User(postData)
                db.user.insert_one(user.__dict__)

                status = 201  # HTTP Request: Created, Only if the user was registered
                responseBody = {
                    'status': 'success',
                    'message': 'Successfully registered user.'
                }
            else:
                status = 401  # HTTP Request: Unauthorized
                responseBody = {
                    'status': 'failed',
                    'message': 'There is already a user registered with the username'  # TODO: Distinguish similarities
                }
        elif '/login' in path:
            # TODO hash + salt password to see if that password is found
            validCredentials = db.user.count_documents({"username": postData["username"],
                                                        "password": postData["password"]})
            if validCredentials > 0:
                status = 200
                responseBody = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'authentication': ''  # TODO Add Authentication token
                }
            else:
                status = 401
                responseBody = {
                    'status': 'failed',
                    'message': 'Failed to find user with provided information'
                }
        self.send_response(status)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        responseString = json.dumps(responseBody).encode('utf-8')
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
