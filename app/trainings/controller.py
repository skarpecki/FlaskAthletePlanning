from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_claims
from sqlalchemy.exc import OperationalError
from app.common.jwt_exceptions_handler import catch_jwt_exceptions

from .service import TrainingService, ExercisesService
from .schema import TrainingSchema, ExerciseSchema, ExerciseUpdateSchema
from .model import Training


class Trainings(Resource):

    @catch_jwt_exceptions
    @jwt_required
    def get(self, training_id):
        try:
            claims = get_jwt_claims()
            Training = TrainingService.get_by_id(training_id, claims)
            return TrainingSchema().dump(Training)
        except ValidationError as err:
            return err.messages
        except AttributeError as err:
            return {"Error": "No such training found"}


    @catch_jwt_exceptions
    @jwt_required
    def put(self, training_id):
        claims = get_jwt_claims()
        try:
            # feedback should be sent as {"feedback": "text"}
            args = request.get_json(force=True)
            return_json = {}
            if 'feedback' in args:
                result = TrainingService.add_feedback(training_id, claims, args['feedback'])
                return_json['feedback'] = result
            if 'date' in args:
                result = TrainingService.modify_date(training_id, claims, args['date'])
                return_json['date'] = result
            return return_json
        except ValidationError as err:
            return err.messages
        except AttributeError as err:
            return {"Error": str(err)}
        except OperationalError as err:
            return {"Error": "Wrong data provided"}


class TrainingsSearch(Resource):

    @catch_jwt_exceptions
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        if not request.args:
            trainings = TrainingService.get_all(claims)
        else:
            try:
                kwargs = TrainingSchema().load(dict(request.args.items()))
                trainings = TrainingService.get_by_args(claims, kwargs)
            except ValidationError as err:
                return err.messages
            except KeyError as err:
                return {"error": "wrong data provided"}
        if len(trainings) != 0:
            return TrainingSchema().dump(trainings, many=True)
        else:
            return {"Message": "No training found"}

    @catch_jwt_exceptions
    @jwt_required
    def post(self):
        claims = get_jwt_claims()
        try:
            attrs = TrainingSchema().load(request.get_json(force=True))
            training_id = TrainingService.create(claims, attrs)
            return {"Created training can be found under":
                    "127.0.0.1:5000/trainings/{}".format(training_id)}
        except ValidationError as err:
            return err.messages



class Exercises(Resource):
    @catch_jwt_exceptions
    @jwt_required
    def get(self, training_id):
        claims = get_jwt_claims()
        try:
            exercises = ExercisesService.get_all(training_id, claims)
            return ExerciseSchema().dump(exercises, many=True)
        except ValidationError as err:
            return err.messages
        except AttributeError as err:
            return {"Error": "No such training found"}

    @catch_jwt_exceptions
    @jwt_required
    def post(self, training_id):
        claims = get_jwt_claims()
        try:
            attrs = ExerciseSchema().load(request.get_json(force=True))
            exercise = ExercisesService.create(training_id, claims, attrs)
            return {"Created exercise can be found under":
                    "127.0.0.1:5000/trainings/{}/exercises".format(training_id)}
        except ValidationError as err:
            return err.messages
        except AttributeError as err:
            return {"Error": "No such training found"}

class ExercisesWithID(Resource):
    @catch_jwt_exceptions
    @jwt_required
    def get(self, training_id, exercise_id):
        claims = get_jwt_claims()
        try:
            exercise = ExercisesService.get_by_id(training_id, exercise_id, claims)
            return ExerciseSchema().dump(exercise)
        except ValidationError as err:
            return err.messages
        except AttributeError as err:
            return {"Error": "No such resource found"}

    @catch_jwt_exceptions
    @jwt_required
    def put(self, training_id, exercise_id):
        claims = get_jwt_claims()
        try:
            attrs = ExerciseUpdateSchema().load(request.get_json(force=True))
            exercise = ExercisesService.update(training_id, exercise_id, claims, **attrs)
            return ExerciseSchema().dump(exercise)
        except ValidationError as err:
            return err.messages
        except AttributeError as err:
            # TODO: two versions, one for debugging (like below), one for prod with some message for user
            return {"Error": str(err)}

    @catch_jwt_exceptions
    @jwt_required
    def delete(self, training_id, exercise_id):
        claims = get_jwt_claims()
        try:
            ExercisesService.delete(training_id, exercise_id, claims)
            return {"message": "Succesfully deleted exercise of id: {}".format(exercise_id)}
        except ValidationError as err:
            return err.messages
        except AttributeError as err:
            print(str(err))
            return {"Error": "No such resource found"}