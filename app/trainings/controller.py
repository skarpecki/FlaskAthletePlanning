from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_claims
from datetime import date

from .service import TrainingService, ExercisesService
from .schema import TrainingSchema, ExerciseSchema
from .model import Training


class Trainings(Resource):
    def get(self, training_id):
        Training = TrainingService.get_by_id(training_id)
        return TrainingSchema().dump(Training)


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
        if claims['role'] != 'coach':
            return {"error": "non authorized access"}, 401
        else:
            try:
                attrs = TrainingSchema().load(request.get_json(force=True))
                if attrs['date'] <= date.today():
                    raise ValidationError(message={"date": "Cannot plan a training for past"})
                training_id = TrainingService.create(claims['userID'], attrs)
                return {"Created training can be found under":
                        "127.0.0.1:5000/trainings/{}".format(training_id)}
            except ValidationError as err:
                return err.messages

class Exercises(Resource):
    def get(self, training_id):
        exercises = ExercisesService.get_by_id(training_id)
        return ExerciseSchema().dump(exercises, many=True)

    def post(self, training_id):
        attrs = ExerciseSchema().load(request.get_json(force=True))
        exercise = ExercisesService.create(training_id, attrs)
        return {"Created exercise can be found under":
                "127.0.0.1:5000/trainings/{}/exercises".format(training_id)}
