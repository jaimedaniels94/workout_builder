from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy 
from os import path

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exercise = db.Column(db.String(200), nullable=False)
    reps = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Workout('{self.exercise}', '{self.reps}')"

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        workout_exercise = request.form['exercise']
        workout_reps = request.form['reps']
        new_workout = Workout(exercise=workout_exercise, reps=workout_reps)
        try:
            db.session.add(new_workout)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem adding your exercise'
    else:
        workouts = Workout.query.all()
        return render_template('index.html', workouts=workouts)

if __name__ == "__main__":
    app.run(debug=True)