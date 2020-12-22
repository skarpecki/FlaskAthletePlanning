from app import db

#TODO:implement training type

class Training(db.Model):
    """Training model class"""

    __tablename__ = "trainings"

    id = db.Column(db.INTEGER, primary_key=True)
    date = db.Column(db.DATETIME, nullable=False)
    athlete_feedback = db.Column(db.String(255), nullable=True)
    coach_feedback = db.Column(db.String(255), nullable=True)
    athletes_id = db.Column(db.INTEGER, db.ForeignKey('users.id'), nullable=False)
    coaches_id = db.Column(db.INTEGER, nullable=False)



class Exercise(db.Model):
    """Exercises model class"""

    __tablename__ = "exercises"

    id = db.Column(db.INTEGER, primary_key=True)
    exercise = db.Column(db.String(50), nullable=False)
    sets = db.Column(db.INTEGER, nullable=False)
    reps = db.Column(db.INTEGER, nullable=False)
    rpe = db.Column(db.FLOAT, nullable=False)
    trainings_id = db.Column(db.INTEGER, nullable=False)
