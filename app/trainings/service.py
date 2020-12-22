from marshmallow import ValidationError

from app import db
from .model import Training
from .model import Exercise

class TrainingService():
    @staticmethod
    def get_all(claims) -> list:
        print(claims['userID'])
        if claims['role'] == 'athlete':
            trainings = Training.query.filter_by(athletes_id=claims['userID']).all()
        else:
            trainings = Training.query.filter_by(coaches_id=claims['userID']).all()
        return trainings


    @staticmethod
    def get_by_args(claims, kwargs):
        if claims['role'] == 'athlete':
            kwargs.pop('athletes_id', None)
            trainings = Training.query.filter_by(athletes_id=claims['userID'], **kwargs).all()
        else:
            kwargs.pop('coaches_id', None)
            trainings = Training.query.filter_by(coaches_id=claims['userID'], **kwargs).all()
        return trainings


    @staticmethod
    def get_by_id(id):
        result = Training.query.get(id)
        return result

    @staticmethod
    def create(coach_id, attrs):
        metadata = db.MetaData()
        metadata.bind = db.engine
        vUserCoach = db.Table("vcoaches_athletes", metadata,
                              db.Column("coach_id", db.Integer, primary_key=True),
                              db.Column("athlete_id", db.Integer, db.ForeignKey("users.id")),
                              autoload=True)
        coach_athlete = db.session.query(vUserCoach).filter(vUserCoach.columns.coach_id == coach_id).all()
        athletes_ids = [t[1] for t in coach_athlete]
        if attrs['athletes_id'] not in athletes_ids:
            raise ValidationError(message={"athleteID": "Provided athlete is not coached by logged in coach"})

        if 'athlete_feedback' in attrs:
            athlete_feedback = attrs['athlete_feedback']
        else:
            athlete_feedback = None

        if 'coach_feedback' in attrs:
            coach_feedback = attrs['coach_feedback']
        else:
            coach_feedback = None
        training = Training(
            date=attrs['date'],
            athlete_feedback=athlete_feedback,
            coach_feedback=coach_feedback,
            athletes_id=attrs['athletes_id'],
            coaches_id=coach_id
        )
        db.session.add(training)
        db.session.commit()

        return training.id



class ExercisesService():
    @staticmethod
    def get_by_id(id):
        result = Exercise.query.filter_by(trainings_id=id).all()
        return result

    @staticmethod
    def create(id, attrs):
        exercise = Exercise(
            exercise=attrs["exercise"],
            sets=attrs["sets"],
            reps=attrs["reps"],
            rpe=attrs["rpe"],
            trainings_id=id
        )
        db.session.add(exercise)
        db.session.commit()

        return exercise