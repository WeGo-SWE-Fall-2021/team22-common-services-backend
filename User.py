from bson.objectid import ObjectId


class User:
    # class constructor, takes a dictionary, which is the JSON passed from the HTTP Post, as an argument and
    # populates class attributes
    def __init__(self, postData):
        # If postData dictionary is coming from mongodb, then we need to extract 
        # the id since it's from an ObjectID class by casting it to a string,
        # Ids should be generated from mongo db
        self._id = str(postData.get("_id", ''))
        self._fname = postData["fname"]
        self._lname = postData["lname"]
        self._phoneNumber = postData["phoneNumber"]
        self._email = postData["email"]
        self._username = postData["username"]
        self._password = postData["password"]

    @property
    def id(self):
        return self._id

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def fname(self):
        return self._fname

    @fname.setter
    def fname(self, value):
        self._fname = value

    @property
    def lname(self):
        return self._lname

    @lname.setter
    def lname(self, value):
        self._lname = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def phoneNumber(self):
        return self._phoneNumber

    @phoneNumber.setter
    def phoneNumber(self, value):
        self._phoneNumber = value
