import datetime as dt
import time

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from marshmallow import Schema, fields, validate, validates_schema, ValidationError

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
  
  @validates('name')
  def validate_name(self, key, name_input):
    if len(name_input) < 1:
      raise ValueError("Name must be more one character")
    return name_input
  
  @validates('category')
  def validate_category(self, key, category_input):
    categories = ['Resistance', 'Cardiovascular', 'Flexibility', 'Balance', 'Sports-Specific']
    if category_input not in categories:
      raise ValueError(f"Must be one of: {','.join(categories)}.")
    return category_input
  
  @validates('equipment_needed')
  def validate_equipment_needed(self, key, eq_needed_input):
    if eq_needed_input is not None and not isinstance(eq_needed_input, bool):
      raise ValueError("Must be true or false")
    return eq_needed_input
  
  def __repr__(self):
    return f'<Exercise {self.id}, {self.name}, {self.category}, {self.equipment_needed}'

# Use Marshmallow Validation to check that category is OneOf 5 types of categories

class ExerciseSchema(Schema):
  id = fields.Int(dump_only=True)
  name = fields.Str(required=True) # cannot be null, none, empty string
  category = fields.Str(validate=validate.OneOf(['Resistance', 'Cardiovascular', 'Flexibility', 'Balance', 'Sports-Specific'])) # redundant but still effective
  equipment_needed = fields.Boolean() 
  
  workout_exercises = fields.List(fields.Nested(lambda: WorkoutExercisesSchema(exclude=('exercise',))))
  
  @validates('equipment_needed')
  def validate_equipment_needed_schema(self, eq_needed):
    if eq_needed is not None and not isinstance(eq_needed, bool):
      raise ValidationError("equipment_needed must be true or false")
    return eq_needed


class Workout(db.Model):
  __tablename__ = 'workouts'
  
  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.Date, nullable=False)
  duration_minutes = db.Column(db.Integer, nullable=False)
  notes = db.Column(db.Text)
  
  # Relationship mapping Workout to Workout_Exercises
  workout_exercises = db.relationship('WorkoutExercises', back_populates='workout')
  
  # Constraint to update an empty string to the default General Workout
  @validates('notes')
  def validates_notes(self, key, notes_input):
    if notes_input == '':
      notes_input = 'General Workout'
    return notes_input
  
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
    return duration
    
  def __repr__(self):
    return f'<Workout {self.id}, {self.date}, {self.duration_minutes}, {self.notes}'

class WorkoutSchema(Schema):
  id = fields.Int(dump_only=True)
  date = fields.Date(format="%Y-%m-%d") # accepts only the correct format
  duration_minutes = fields.Int(required=True, validate=validate.Range(min=1, max=210)) # No longer than 3.5 hours 
  notes = fields.Str(load_default='General Workout', dump_default='General Workout')   # Default to General Workout if not input is provided
  
  workout_exercises = fields.List(fields.Nested(lambda: WorkoutExercisesSchema(exclude=('workout',))))
  
  # Schema validation that ensures workout date is not in the future
  @validates_schema
  def validate_schema(self, data, **kwargs):
    today = dt.date.today()
    if data['date'] > today:
      raise ValidationError(f'Date of the workout cannot be in the future') 

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
  duration_seconds = db.Column(db.Integer, nullable=False)
  
  # Relationship mapping WorkoutExercises to related workout
  workout = db.relationship('Workout', back_populates='workout_exercises')
  # Relationship mapping WorkoutExercises to relates exercise
  exercise = db.relationship('Exercise', back_populates='workout_exercises')
  
  # Model-level check 
  @validates('reps', 'sets', 'duration_seconds')
  def validate_input(self, key, input):
    # Check for presence and not an empty input
    if not input:
      raise ValueError("Input must be present")
    # Check for the correct type using isinstance
    if not isinstance(input, int):
      raise ValueError("Input must be a number")
    if input <= 0:
      raise ValueError("Input must be a positive number")
    return input
  
  def __repr__(self):
    return f'Workout Exercises {self.id}, {self.workout}, {self.exercise}, {self.reps}, {self.sets}, {self.duration_seconds}'
  
class WorkoutExercisesSchema(Schema):
  id = fields.Int(dump_only=True)
  reps = fields.Int(required=True, validate=validate.Range(min=1, max=100)) # No more than 100 reps
  sets = fields.Int(required=True, validate=validate.Range(min=1, max=20)) # No more than 20 sets
  duration_seconds = fields.Int(required=True, validate=validate.Range(min=1, max=18000)) # No longer than 5 hours
  
  exercise = fields.Nested(ExerciseSchema(exclude=('workout_exercises',)))
  workout = fields.Nested(WorkoutSchema(exclude=('workout_exercises',)))