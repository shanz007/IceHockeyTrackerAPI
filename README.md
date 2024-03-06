# PWP SPRING 2024
# Group information

* Student 1. Md Mobusshar Islam \<mislam23@student.oulu.fi\>
* Student 2. Emmanuel Ikwunna \<emmanuel.ikwunna@student.oulu.fi\>
* Student 3. Shanaka Badde Liyanage Don \<shanaka.baddeliyanagedon@student.oulu.fi\>

# Ice hockey Tracker API

## IceHockeyTrackerAPI Dependecy Information & Installation*

This is a Python3 based project that uses python related libraries such as  flask, flask_sqlalchemy etc
All of the dependencies can be found in the file icehockeytracker/requirements.txt from the root directory of the project.

For Cloing the project using below command

 	git clone https://github.com/shanz007/IceHockeyTrackerAPI.git

For Installing dependencies, please execute 

	pip install -r requirements.txt

For configurations
	
 	export FLASK_ENV=development
	export FLASK_APP=icehockeytracker

## Database Dependecy Information & Setup 

	The database engine used is SQLite, version 3.40.1.

### Database Setup Instructions : initilaization & population

For IceHockeyTrackerAPI system, we using SQLite3 as our database. please find the below commands for initialization, populization with some random test data to check the integrity 
between each database relations and models. 


Database Initilisation

	flask --app icehockeytracker init-db


Database data populization 

	flask --app icehockeytracker db-populate
	

All the python scripts for above tasks are listed in the model.py file. The populated db file can be found in the icehockeytracker/instance/ subfolder.


## Start API Server 

Upon success of the above database steps , the API Server can be invoked by executing

	
	flask --app icehockeytracker runs

 	Access the server http://127.0.0.1:5000/


     
## API Server Testing & Test Coverage

All of the test dependencies can be found in the file : test/requirements.txt from the root directory of the project. for testing **pytest and pytest-cov** are used specifically.
test folder includes model classes that have been tested

	flask --app icehockeytracker test

For testing with coverage 

	pytest --cov-report term-missing --cov=icehockeytracker
 

## API Server Code quality compliance 

For code quality and compliance, we have used pylint  

 	pylint icehockeytracker


## API Server documentation 

All of the documentation dependencies can be found in the main requirement.txt. we have used flasgger and pyyaml

	For Swagger API documentation  :  http://127.0.0.1:5000/apidocs/


