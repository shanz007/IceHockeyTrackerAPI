# PWP Spring 2024

![GitHub commit activity](https://img.shields.io/github/commit-activity/t/shanz007/IceHockeyTrackerAPI)
![GitHub last commit](https://img.shields.io/github/last-commit/shanz007/IceHockeyTrackerAPI)
![GitHub top language](https://img.shields.io/github/languages/top/shanz007/IceHockeyTrackerAPI)
![GitHub language count](https://img.shields.io/github/languages/count/shanz007/IceHockeyTrackerAPI)
![GitHub License](https://img.shields.io/github/license/shanz007/IceHockeyTrackerAPI)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/shanz007/IceHockeyTrackerAPI)
![GitHub repo size](https://img.shields.io/github/repo-size/shanz007/IceHockeyTrackerAPI)
![GitHub forks](https://img.shields.io/github/forks/shanz007/IceHockeyTrackerAPI)
![GitHub Repo stars](https://img.shields.io/github/stars/shanz007/IceHockeyTrackerAPI)

## Group Information

- **Student 1:** Md Mobusshar Islam \<mislam23@student.oulu.fi\>
- **Student 2:** Emmanuel Ikwunna \<emmanuel.ikwunna@student.oulu.fi\>
- **Student 3:** Shanaka Badde Liyanage Don \<shanaka.baddeliyanagedon@student.oulu.fi\>

## Ice Hockey Tracker API

### Overview

The Ice Hockey Tracker API is a Python 3-based project leveraging Flask and Flask-SQLAlchemy among other libraries. The project dependencies are detailed in [requirements.txt](https://github.com/shanz007/IceHockeyTrackerAPI/blob/main/requirements.txt) at the root directory.

### Getting Started

#### Cloning the Repository

To clone the project, use the following command:

```sh
git clone https://github.com/shanz007/IceHockeyTrackerAPI.git
```

#### Installing Dependencies

Navigate to the project directory and install the required dependencies:

```sh
pip install -r requirements.txt
```

#### Configuration

Set up the environment variables:

```sh
export FLASK_ENV=development
export FLASK_APP=icehockeytracker
```

### Database Setup

This project uses SQLite (version 3.40.1) as its database engine.

#### Initialization and Population

To initialize and populate the database with sample data:

**Initialization:**

```sh
flask --app icehockeytracker init-db
```

**Population with Sample Data:**

```sh
flask --app icehockeytracker db-populate
```

The database scripts are located in `model.py`, and the populated database file is stored under `icehockeytracker/instance/`.

### Running the API Server

After completing the database setup, start the API server with:

```sh
flask --app icehockeytracker run
```

The server will be accessible at <http://127.0.0.1:5000/>.

### Testing and Coverage

For testing, this project uses pytest and pytest-cov, found in `test/requirements.txt`. To run tests:

```sh
flask --app icehockeytracker test
```

For coverage reports:

```sh
pytest --cov-report term-missing --cov=icehockeytracker
```

### Code Quality

Pylint is used for ensuring code quality and compliance:

```sh
pylint icehockeytracker
```

### API Documentation

API documentation is generated with Flasgger and PyYAML, included in the main `requirements.txt`. Access the Swagger UI documentation at <http://127.0.0.1:5000/apidocs/>.
