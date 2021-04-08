from uuid import uuid4

class User:
    version = "0.1.2"

    # class constructor, takes a dictionary, which is the JSON passed from the HTTP Post, as an argument and
    # populates class attributes
    def __init__(self, dict):
        # If postData dictionary is coming from mongodb, then we need to extract 
        # the id since it's from an ObjectID class by casting it to a string,
        # Ids should be generated from mongo db
        self._id = str(dict.get("_id", uuid4()))
        self._firstName = dict["firstName"]
        self._lastName = dict["lastName"]
        self._phoneNumber = dict["phoneNumber"]
        self._email = dict["email"]
        self._username = dict["username"]
        self._password = dict["password"]

    @property
    def id(self):
        return self._id

    @property
    def firstName(self):
        return self._firstName

    @firstName.setter
    def firstName(self, value):
        self._firstName = value

    @property
    def lastName(self):
        return self._lastName

    @lastName.setter
    def lastName(self, value):
        self._lastName = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def phoneNumber(self):
        return self._phoneNumber

    @phoneNumber.setter
    def phoneNumber(self, value):
        self._phoneNumber = value

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value
