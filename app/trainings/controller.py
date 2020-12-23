from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_claims

from .service import TrainingService, ExercisesService
from .schema import TrainingSchema, ExerciseSchema
from .model import Training


class Trainings(Resource):
    @jwt_required
    def get(self, training_id):
        claims = get_jwt_claims()
        try:
            Training = TrainingService.get_by_id(training_id, claims)
            return TrainingSchema().dump(Training)
        except ValidationError as err:
            return err.message
        except AttributeError as err:
            # TODO: LOG Exception {"Error": str(err)}
            return {"Error": "No such training found"}


#TODO: catch jwt exceptions
class TrainingsSearch(Resource):
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
            return {"Message": "No data found"}

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
    @jwt_required
    def get(self, training_id):
        try:
            claims = get_jwt_claims()
            exercises = ExercisesService.get_by_id(training_id, claims)
            return ExerciseSchema().dump(exercises, many=True)
        except ValidationError as err:
            return err.messages

    @jwt_required
    def post(self, training_id):
        try:
            claims = get_jwt_claims()
            attrs = ExerciseSchema().load(request.get_json(force=True))
            exercise = ExercisesService.create(training_id, claims, attrs)
            return {"Created exercise can be found under":
                    "127.0.0.1:5000/trainings/{}/exercises".format(training_id)}
        except ValidationError as err:
            return err.messages
        except AttributeError as err:
            #TODO: LOG Exception {"Error": str(err)}
            return {"Error": "No such training found"}

