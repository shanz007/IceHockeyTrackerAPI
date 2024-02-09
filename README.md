# PWP SPRING 2024

# Ice hockey Tracker API

# Group information

* Student 1. Md Mobusshar Islam \<mislam23@student.oulu.fi\>
* Student 2. Emmanuel Ikwunna \<emmanuel.ikwunna@student.oulu.fi\>
* Student 3. Shanaka Badde Liyanage Don \<shanaka.baddeliyanagedon@student.oulu.fi\>

__Remember to include all required documentation and HOWTOs, including how to create and populate the database, how to run and test the API, the url to the entrypoint and instructions on how to setup and run the client__




**IceHockeyTrackerAPI Database Setup**


Database Setup Instructions : initilaization & population

For IceHockeyTrackerAPI system, we using SQLite3 as our database. please find the below commands for initialization, populization with some random test data to check the intergrity 
between each dtabase relations or models. 


Database Initiliation

	flask --app icehockeytracker init-db


Database data populization 


	flask --app icehockeytracker db-populate
	

All the python scripts for above tasks are listed in the model.py file. The populated db file can be found in the icehockeytracker/instance/ subfolder.




**IceHockeyTrackerAPI Dependecy Information & Installation**


These dependencies can be found in the file icehockeytracker/requirements.txt from the root directory of the project.


The database engine used is SQLite, version 3.40.1.


For Installing dependencies, please execute

	pip install -r requirements.txt

