from marshmallow import ValidationError
from datetime import date
from dateutil.parser import parse

from app import db
from .model import Training
from .model import Exercise
from app.common.logger import Logger
from datetime import datetime

class TrainingService():
    @staticmethod
    def get_all(claims) -> list:
        print(claims['userID'])
        if claims['role'] == 'athlete':
            trainings = Training.query.filter_by(athletes_id=claims['userID']).all()
        elif claims['role'] == 'coach':
            trainings = Training.query.filter_by(coaches_id=claims['userID']).all()
        return trainings


    @staticmethod
    def get_by_args(claims, kwargs):
        if claims['role'] == 'athlete':
            # if user will ask for trainings other than his it will be ignored and his training will be loaded
            kwargs.pop('athletes_id', None)
            trainings = Training.query.filter_by(athletes_id=claims['userID'], **kwargs).all()
        else:
            kwargs.pop('coaches_id', None)
            trainings = Training.query.filter_by(coaches_id=claims['userID'], **kwargs).all()
        return trainings


    @staticmethod
    def get_by_id(training_id, claims):
        training = Training.query.get(training_id)
        if training.athletes_id == claims['userID'] or training.coaches_id == claims['userID']:
            return training
        else:
            raise ValidationError(message={"ID": "User doesn't have access to that training"})

    @staticmethod
    def create(claims, attrs):
        if claims['role'] != 'coach':
            raise ValidationError(message={"Role": "Only coach can create a training"})
        if attrs['date'] <= date.today():
            raise ValidationError(message={"date": "Cannot plan a training for past"})

        metadata = db.MetaData()
        metadata.bind = db.engine
        vUserCoach = db.Table("vcoaches_athletes", metadata,
                              db.Column("coach_id", db.Integer, primary_key=True),
                              db.Column("athlete_id", db.Integer, db.ForeignKey("users.id")),
                              autoload=True)
        coach_athlete = db.session.query(vUserCoach).filter(vUserCoach.columns.coach_id == claims['userID']).all()
        athletes_ids = [t[1] for t in coach_athlete]

        trainings = Training.query.filter_by(athletes_id=attrs['athletes_id']).all()
        # can add training only if athlete coached by logged in coach and if it is first training of particular athlete
        # second is required as it won't be possible to add first training otherwise, as vUserCoach is based on trainings table
        if attrs['athletes_id'] not in athletes_ids and len(trainings) != 0:
            raise ValidationError(message={"athleteID": "Provided athlete is not coached by logged in coach"})


        training = Training(
            date=attrs['date'],
            athletes_id=attrs['athletes_id'],
            coaches_id=claims['userID']
        )
        db.session.add(training)
        db.session.commit()

        #for key, item in attrs.items():
        #    Logger.log_message(claims['userID'], 'trainings', key, 'null', item)
        #logging only id instead of all attributes
        Logger.log_message(claims['userID'], 'trainings', 'id', 'null', training.id)

        return training.id



    @staticmethod
    def add_feedback(training_id, claims, feedback):
        training = Training.query.get(training_id)
        if claims['role'] == 'coach' and training.coaches_id == claims['userID']:
            old_feedback = "null" if training.coach_feedback is None else training.coach_feedback
            training.coach_feedback = feedback
            db.session.commit()
            Logger.log_message(claims['userID'], 'trainings', 'coach_feedback', old_feedback,
                               training.coach_feedback)
            return feedback
        elif claims['role'] == 'athlete' and training.athletes_id == claims['userID']:
            old_feedback = "null" if training.athlete_feedback is None else training.athlete_feedback
            training.athlete_feedback = feedback
            db.session.commit()
            Logger.log_message(claims['userID'], 'trainings', 'athlete_feedback', old_feedback,
                               training.athlete_feedback)
            return feedback
        else:
            raise ValidationError(message={"ID": "User doesn't have access to training"})

    @staticmethod
    def modify_date(training_id, claims, new_date):
        #new_date is passed as str, hence need to parse it
        new_date = parse(new_date).date()
        if new_date <= date.today():
            raise ValidationError(message={"date": "Cannot plan a training for past"})
        training = Training.query.get(training_id)
        if claims['role'] == 'coach' and training.coaches_id == claims['userID']:
            old_date = training.date
            training.date = new_date
            db.session.commit()
            Logger.log_message(claims['userID'], 'trainings', 'date',
                               old_date, training.date)
            return str(new_date)
        else:
            raise ValidationError(message={"ID": "User doesn't have access to training"})

class ExercisesService:
    @staticmethod
    def get_all(training_id, claims):
        ExercisesService.validate(training_id, claims)
        result = Exercise.query.filter_by(trainings_id=training_id).all()
        return result

    @staticmethod
    def get_by_id(training_id, exercise_id, claims):
        ExercisesService.validate(training_id, claims)
        exercise = Exercise.query.filter_by(id=exercise_id, trainings_id=training_id).first()
        return exercise

    @staticmethod
    def create(training_id, claims, attrs):
        if claims['role'] == 'athlete':
            raise ValidationError(message={"ID": "Athlete cannot insert exercise"})
        ExercisesService.validate(training_id, claims)
        exercise = Exercise(
            exercise=attrs["exercise"],
            sets=attrs["sets"],
            reps=attrs["reps"],
            rpe=attrs["rpe"],
            trainings_id=training_id
        )
        db.session.add(exercise)
        db.session.commit()
        #for key, item in attrs.items():
        #    Logger.log_message(claims['userID'], 'exercises', key, "null", item)
        # logging only id instead of all attributes
        Logger.log_message(claims['userID'], 'exercises', 'id', 'null', exercise.id)

        return exercise

    @staticmethod
    def update(training_id, exercise_id, claims, **kwargs):
        if claims['role'] == 'athlete':
            raise ValidationError(message={"ID": "Athlete cannot update exercise"})
        ExercisesService.validate(training_id, claims)
        exercise = Exercise.query.filter_by(id=exercise_id, trainings_id=training_id).first()
        if exercise is None:
            raise ValidationError(message={"exerciseID": "Exercise of provided ID doesn't exist"})
        old_kwargs = {}
        for key, item in kwargs.items():
            old_kwargs[key] = getattr(exercise, key, "null")
            setattr(exercise, key, item)
        db.session.commit()
        # having two for loops as event can be logged only after committing (possibility of exception)
        for key, item in kwargs.items():
            #log only if any change occured
            if old_kwargs[key] != kwargs[key]:
                Logger.log_message(claims['userID'], 'exercises', key, old_kwargs[key], kwargs[key])
        return exercise

    @staticmethod
    def delete(training_id, exercise_id, claims):
        if claims['role'] == 'athlete':
            raise ValidationError(message={"ID": "Athlete cannot remove exercise"})
        ExercisesService.validate(training_id, claims)
        db.session.query(Exercise).filter_by(id=exercise_id, trainings_id=training_id).delete(synchronize_session='fetch')
        db.session. commit()
        Logger.log_message(claims['userID'], "exercises", "id", exercise_id, "null")
        return exercise_id

    @staticmethod
    def validate(training_id, claims):
        training = Training.query.get(training_id)
        if claims['role'] == 'coach' and training.coaches_id != claims['userID']:
            raise ValidationError(message={"ID": "User doesn't have access to the training provided"})
        elif claims['role'] == 'athlete' and training.athletes_id != claims['userID']:
            raise ValidationError(message={"ID": "User doesn't have access to the training provided"})
