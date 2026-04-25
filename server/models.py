from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates

metadata = MetaData()

db = SQLAlchemy(metadata=metadata)

class Exercise(db.Model):
  __tablename__ = 'exercises'
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False, unique=True)
  category = db.Column(db.String, nullable=False)
  equipment_needed = db.Column(db.Boolean)
  
  # Relationship maaping the exercise to Workout_exercises
  workout_exercises = db.relationship('WorkoutExercises', back_populates='exercise')
  
  # Use Marshmallow Validation to check that category is OneOf 5 types of categories
  ####
  
  def __repr__(self):
    return f'<Exercise {self.id}, {self.name}, {self.category}, {self.equipment_needed}'
  
class Workout(db.Model):
  __tablename__ = 'workouts'
  
  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.Date, nullable=False)
  duration_minutes = db.Column(db.Integer, nullable=False)
  notes = db.Column(db.Text)
  
  # Relationship mapping Workout to Workout_Exercises
  workout_exercise = db.relationship('WorkoutExercises', back_populates='workout')
  
  # Model-level check 
  @validates('duration_minutes')
  def validates_duration_minutes(self, key, duration):
    # checks for presence
    if not duration:
      raise ValueError("Duration in minutes must be present")
    # Check for the correct type using isinstance
    if not isinstance(duration, int):
      raise ValueError("Duration in minutes must be a number")
    # checks that one workout is not longer than 3 hours  
    if duration > 210:
      raise ValueError("Workout cannot be longer than 3.5 hours/210 minutes ")
    
  def __repr__(self):
    return f'<Workout {self.id}, {self.date}, {self.duration_minutes}, {self.notes}'


# JOIN model to store many-to-many relationship between exercise and workout
class WorkoutExercises(db.Model):
  __tablename__ = 'workout_exercises'
  
  id = db.Column(db.Integer, primary_key=True)
  # Foreign key to store Workout
  workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'))
  # Foreign key to store Exercise
  exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'))
  reps = db.Column(db.Integer, nullable=False)
  sets = db.Column(db.Integer, nullable=False)
  duration_secs = db.Column(db.Integer, nullable=False)
  
  # Relationship mapping WorkoutExercises to related workout
  workout = db.relationship('Workout', back_populates='workout_exercises')
  # Relationship mapping WorkoutExercises to relates exercise
  exercise = db.relationship('Exercise', back_populates='workout_exercises')
  
  # Model-level check 
  @validates('reps', 'sets', 'duration_secs')
  def validate_input(self, key, input):
    # Check for presence and not an empty input
    if not input:
      raise ValueError("Input must be present")
    # Check for the correct type using isinstance
    if not isinstance(input, int):
      raise ValueError("Input must be a number")
  
  def __repr__(self):
    return f'Workout Exercises {self.id}, {self.workout}, {self.exercise}, {self.reps}, {self.sets}, {self.duration_secs}'
  
