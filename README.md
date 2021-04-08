# Team 22 Common Services Back end
This is the Team 22 backend for common services. This repository deals with any requests handled in `/api/v1/common-services/[request-name]/` for both `demand` and `supply` services.

## Objective ##
The objective of `Common Services Backend` is to be able to reduce duplicate code that would have been in both separate systems and instead with this repository we can manage in one repository. 

This repository includes `unittest` so that we are able to test our objects and soon we will implement CI/CD for  automated builds and testing.

## REST API for Common Services ## 
You can view working REST api using [Postman](https://www.getpostman.com/collections/cad786a00f31ea7893bd)

## Structure ##
```
team22-common-services-backend
├── docs                        # Documentation Directory
├── unittest                    # Unit Test Directory to test Object classes                     
│   └── user_test_case.py       # Test cases for `User.py` class
├── mongoutils.py               # Helper class for MongoDB
├── user.py                     # User class object
├── server.py                   # The main Python endpoints server
├── requirements.txt            # Python Dependencies to run `server.py`
└── README.md                   # Documentation about this repo
```

> Use short lowercase names for files and folders except for
> `README.md`


## Modifying This Repo ##
### Cloning repository ###
***Before you star you must have Python 3.8 installed in your system***  
If you would like to contribute to this repository, you first must clone this repository by running:  
```git clone https://bitbucket.org/swe-spring-2021-team-22/team22-common-services.git```  
  
### Setting Up Environment
After doing so, go to the `team22-common-services` directory using command line or PyCharm Terminal and we will install the `env` environment for your setup by running:  
`python3 -m venv env`  
  
### Activating Environment
Now that you have the environment, in order to be in the environment you type:  
`source env/bin/activate`  
  
### Dependencies ###

#### Installation ####
In order to install dependencies, you need to make sure you are on the project directory. Once you are there, execute `python3 -m pip install -r requirements.txt`.

#### Update/Remove dependencies ####
If you added or removed dependencies in your project and need to include those dependencies you need to generate a new `requirements.txt` file. You do so by running `pip freeze > requirements.txt`.

### .env file ###
This file you have to make on your own. It should be on the project directory. If you notice, `MongoUtils.py` script uses `MONGO_SECRET`, which needs to be defined in `.env` file. This holds our mongo database `developer` password.

### Deactivating Environment
Now you should be in the `env` environment. To get out of the environment you type `deactivate` in command line.
