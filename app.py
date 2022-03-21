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

@app.route('/delete/<int:id>')
def delete(id):
    exercise_to_delete = Workout.query.get_or_404(id)

    try:
        db.session.delete(exercise_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting the exercise'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    workout = Workout.query.get_or_404(id)

    if request.method == 'POST':
        workout.exercise = request.form['exercise']
        workout.reps = request.form['reps']

        try:
            db.session.commit()
            return redirect('/')

        except:
            return 'There was a problem updating the exercise'
    else:
        return render_template('update.html', workout=workout)


if __name__ == "__main__":
    app.run(debug=True)