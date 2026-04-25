import datetime
from app import app
from models import db, Exercise, Workout, WorkoutExercises

with app.app_context():
  # Delete all rows in current tables
  Exercise.query.delete()
  Workout.query.delete()
  WorkoutExercises.query.delete()
  
  # Create Exercises
  # types = ['Resistance', 'Cardiovascular', 'Flexibility', 'Sports-Specific']
  e1 = Exercise(name='Downward Facing Dog', category='Flexibility', equipment_needed=True)
  e2 = Exercise(name='Cat Cow',category='Flexibility', equipment_needed=True)
  e3 = Exercise(name='Push up', category='Resistance', equipment_needed=False)
  e4 = Exercise(name='Lunge', category='Resistance', equipment_needed=False)
  e5 = Exercise(name='Mountain Climber', category='Cardiovascular', equipment_needed=True)
  db.session.add_all([e1, e2, e3, e4, e5])
  db.session.commit()
  
  # Create Workouts
  w1 = Workout(date=datetime.datetime(2026, 4, 17), duration_minutes=15, notes='Yoga flow')
  w2 = Workout(date=datetime.datetime(2026, 10, 30), duration_minutes=20, notes='Strength training')
  db.session.add_all([w1, w2])
  db.session.commit()
  
  # Create Many to Many relationship between exercises and workouts
  db.session.add(WorkoutExercises(reps=5, sets=2, duration_seconds=10, workout=w1, exercise=e1))
  db.session.add(WorkoutExercises(reps=10, sets=1, duration_seconds=5, workout=w1, exercise=e2))
  db.session.add(WorkoutExercises(reps=10, sets=2, duration_seconds=3, workout=w1, exercise=e3))
  db.session.add(WorkoutExercises(reps=5, sets=2, duration_seconds=10, workout=w1, exercise=e4))
      
  db.session.add(WorkoutExercises(reps=10, sets=5, duration_seconds=3, workout=w2, exercise=e3))  
  db.session.add(WorkoutExercises(reps=10, sets=3, duration_seconds=5, workout=w2, exercise=e4))
  db.session.add(WorkoutExercises(reps=20, sets=2, duration_seconds=10, workout=w2, exercise=e5))   
  db.session.commit()  
  
  print("🌱 Database seeded successfully!")