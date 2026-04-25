from flask import Flask, make_response
from flask_migrate import Migrate
from models import db, Workout, Exercise, WorkoutExercises


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Diplay JSON key/value pairs on separate lines
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
  body = {'message': 'Workout Management using Flask SQLAlchemy'}
  return make_response(body, 200)

# API ENDPOINTS / VIEWS




if __name__ == '__main__':
  app.run(port=5555, debug=True)