from flask import Flask, make_response, jsonify, abort, request
from flask_migrate import Migrate
from datetime import datetime
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

## API ENDPOINTS / VIEWS

# GET /workouts
@app.route('/workouts', methods=["GET"])
def get_workouts():
  workouts = []
  
  for workout in Workout.query.all():
    workout_dict = {
      'id': workout.id,
      'date': workout.date,
      'duration_minutes': workout.duration_minutes,
      'notes': workout.notes if workout.notes else 'General Workout, no notes provided'
    }
    workouts.append(workout_dict)
    
  return jsonify(workouts), 200

# GET /workouts/<id>
@app.route('/workouts/<int:id>', methods=["GET"])
def get_workout(id):
  workout = Workout.query.filter(Workout.id == id).first()
  
  if not workout:
    return jsonify({'error': 'Workout not found'}), 404
  
  else:
    workout_dict = {
      'id': workout.id,
      'date': workout.date,
      'duration_minutes': workout.duration_minutes,
      'notes': workout.notes if workout.notes else 'General Workout, no notes provided'
    }
  
  return jsonify(workout_dict), 200

# POST /workouts
@app.route('/workouts', methods=["POST"])
def create_new_workout():
  if not request.json:
    abort(400, description="Missing JSON data")
  try:
    # Extract data
    data = request.json
    
    # Parse date string into Python date object
    date_str = data.get('date')
    if date_str:
      parsed_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    else:
      parsed_date = None
    
    # Create new Workout object with data
    new_workout = Workout(
      date = parsed_date,
      duration_minutes = data.get('duration_minutes'),
      notes = data.get('notes')
    )
    
    # Add to session and commit to add to database (persistance)
    db.session.add(new_workout)
    db.session.commit()
    
    # Return the newly created workout
    workout_dict = {
      'id': new_workout.id,
      'date': new_workout.date,
      'duration_minutes': new_workout.duration_minutes,
      'notes': new_workout.notes
    }
    return jsonify(workout_dict), 201
  except ValueError as e:
    db.session.rollback()
    abort(400, description=str(e))
  except Exception as e:
    db.session.rollback()
    abort(500, description=str(e))
        
# DELETE /workouts/<id>
@app.route('/workouts/<int:id>', methods=["DELETE"])
def delete_workout(id):
  workout = Workout.query.filter(Workout.id == id).first()
  
  if not workout:
    return jsonify({'error': 'Workout not found'}), 404
  
  try:
    db.session.delete(workout)
    db.session.commit()
    return jsonify({'message': 'Workout deleted successfully'}), 200
    
  except Exception as e:
    db.session.rollback()
    abort(500, description=str(e))


# GET /exercises
@app.route('/exercises', methods=["GET"])
def get_exercises():
  exercises = []
  
  for exercise in Exercise.query.all():
    exercise_dict = {
      'id': exercise.id,
      'name': exercise.name,
      'category': exercise.category,
      'equipment_needed': exercise.equipment_needed
    }
    exercises.append(exercise_dict)
    
  return jsonify(exercises), 200

# GET /exercises/<id>
@app.route('/exercises/<int:id>', methods=["GET"])
def get_exercise(id):
  exercise = Exercise.query.filter(Exercise.id == id).first()
  
  if not exercise:
    return jsonify({'error': 'Exercise not found'}), 404
  
  else:
    exercise_dict = {
      'id': exercise.id,
      'name': exercise.name,
      'category': exercise.category,
      'equipment_needed': exercise.equipment_needed
    }
  
  return jsonify(exercise_dict), 200

# POST /exercises
@app.route('/exercises', methods=["POST"])
def create_new_exercise():
  if not request.json:
    abort(400, description="Missing JSON data")
  try:
    # Extract data
    data = request.json
    
    # Create new Workout object with data
    new_exercise = Exercise(
      name = data.get('name'),
      category = data.get('category'),
      equipment_needed = data.get('equipment_needed')
    )
    
    # Add to session and commit to add to database (persistance)
    db.session.add(new_exercise)
    db.session.commit()
    
    # Return the newly created exercise
    exercise_dict = {
      'id': new_exercise.id,
      'name': new_exercise.name,
      'category': new_exercise.category,
      'equipment_needed': new_exercise.equipment_needed
    }
    return jsonify(exercise_dict), 201
  except ValueError as e:
    db.session.rollback()
    abort(400, description=str(e))
  except Exception as e:
    db.session.rollback()
    abort(500, description=str(e))

# DELETE /exercises/<id>
@app.route('/exercises/<int:id>', methods=["DELETE"])
def delete_exercise(id):
  exercise = Exercise.query.filter(Exercise.id == id).first()
  
  if not exercise:
    return jsonify({'error': 'Exercise not found'}), 404
  
  try:
    db.session.delete(exercise)
    db.session.commit()
    return jsonify({'message': 'Exercise deleted successfully'}), 200
    
  except Exception as e:
    db.session.rollback()
    abort(500, description=str(e))

# POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises
@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=["POST"])
def create_exercise_to_workout(workout_id, exercise_id):
  workout = Workout.query.filter(Workout.id == workout_id).first()
  
  if not workout:
    return jsonify({'error': 'Workout not found'}), 404
  
  exercise = Exercise.query.filter(Exercise.id == exercise_id).first()
  
  if not exercise:
    return jsonify({'error': 'Exercise not found'}), 404
  
  if not request.json:
    abort(400, description="Missing JSON data")
  
  try:
    # Extract data
    data = request.json
    
    # Create new WorkoutExercises object with data
    new_workout_exercise = WorkoutExercises(
      workout_id=workout_id,
      exercise_id=exercise_id,
      reps=data.get('reps'),
      sets=data.get('sets'),
      duration_seconds=data.get('duration_seconds')
    )
    
    # Add to session and commit to add to database
    db.session.add(new_workout_exercise)
    db.session.commit()
    
    # Return the newly created workout exercise
    workout_exercise_dict = {
      'id': new_workout_exercise.id,
      'workout_id': new_workout_exercise.workout_id,
      'exercise_id': new_workout_exercise.exercise_id,
      'reps': new_workout_exercise.reps,
      'sets': new_workout_exercise.sets,
      'duration_seconds': new_workout_exercise.duration_seconds
    }
    return jsonify(workout_exercise_dict), 201
  
  except ValueError as e:
    db.session.rollback()
    abort(400, description=str(e))
  except Exception as e:
    db.session.rollback()
    abort(500, description=str(e))

if __name__ == '__main__':
  app.run(port=5555, debug=True)