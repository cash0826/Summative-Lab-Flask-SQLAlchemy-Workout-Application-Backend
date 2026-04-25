# Summative-Lab-Flask-SQLAlchemy-Workout-Application-Backend
[Project Description] This lab will follow a many-to-many relationship type, since exercises can be associated to many workouts and workouts can be associated to many exercises

## Installation

Run `pipenv install` to create your virtual environment and install dependencies. 
Run `pipenv shell` to enter the virtual environment.

```console
pipenv install && pipenv shell
```

Change to the Server directory and configure the the Flask App environment variables:
```console
cd server
export FLASK_APP=app.py
export FLASK_RUN_PORT=5555
```

To get create the database from the initial migration, run:

```console
flask db upgrade
python seed.py
```
To open and view the backend, ensure you are in the server directory and run either commands:
```console
flask run
python app.py
```

# API Endpoints

* GET /workouts
* GET /workouts/<id>
* POST /workouts
* DELETE /workouts/<id>

* GET /exercises
* GET /exercises/<id>
* POST /exercises
* DELETE /exercises/<id>

* POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises

