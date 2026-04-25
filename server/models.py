from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

metadata = MetaData()

db = SQLAlchemy(metadata=metadata)

class Exercise(db.Model):
  __tablename__ = 'exercises'
  
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  category = db.Column(db.String)
  equipment_needed = db.Column(db.Boolean)
  
  # Relationship maaping the exercise to Workout_exercises
  workout_exercises = db.relationship('WorkoutExercises', back_populates='exercise')
  
  def __repr__(self):
    return f'<Exercise {self.id}, {self.name}, {self.category}, {self.equipment_needed}'
  
class Workout(db.Model):
  __tablename__ = 'workouts'
  
  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.Date)
  duration_minutes = db.Column(db.Integer)
  notes = db.Column(db.Text)
  
  # Relationship mapping Workout to Workout_Exercises
  workout_exercise = db.relationship('WorkoutExercises', back_populates='workout')
  
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
  reps = db.Column(db.Integer)
  sets = db.Column(db.Integer)
  duration_secs = (db.Integer)
  
  # Relationship mapping WorkoutExercises to related workout
  workout = db.relationship('Workout', back_populates='workout_exercises')
  # Relationship mapping WorkoutExercises to relates exercise
  exercise = db.relationship('Exercise', back_populates='workout_exercises')
  
  def __repr__(self):
    return f'Workout Exercises {self.id}, {self.workout}, {self.exercise}, {self.reps}, {self.sets}, {self.duration_secs}'