class User:

    # class constructor, takes a dictionary, which is the JSON passed from the HTTP Post, as an argument and
    # populates class attributes
    def __init__(self, postData):
        self.username = postData["username"]
        self.fName = postData["fname"]
        self.lName = postData["lname"]
        self.email = postData["email"]
        self.address = postData["address"]
        self.password = postData["password"]
        self.phoneNumber = postData["phoneNumber"]

    # basic set methods
    def setUsername(self, username):
        self.username = username

    def setfName(self, fName):
        self.fName = fName

    def setlName(self, lName):
        self.lName = lName

    def setDOB(self, dob):
        self.dob = dob

    def setEmail(self, email):
        self.email = email

    def setAddress(self, address):
        self.address = address

    def setPassword(self, password):
        self.password = password

    def setPhoneNumber(self, phoneNumber):
        self.phoneNumber = phoneNumber

    # basic get methods
    def getUsername(self):
        return self.username

    def getfName(self):
        return self.fName

    def getlName(self):
        return self.lName

    def getDOB(self):
        return self.dob

    def getEmail(self):
        return self.email

    def getAddress(self):
        return self.address

    def getPassword(self):
        return self.password

    def getPhoneNumber(self):
        return self.phoneNumber
