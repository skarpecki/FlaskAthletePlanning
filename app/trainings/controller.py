from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_claims

from .service import TrainingService, ExercisesService
from .schema import TrainingSchema, ExerciseSchema
from .model import Training


class Trainings(Resource):
    def get(self, id):
        print(id)
        Training = TrainingService.get_by_id(id)
        return TrainingSchema().dump(Training)


#TODO: catch jwt exceptions
class TrainingsSearch(Resource):
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        if not request.args:
            if claims['role'] == 'athlete':
                trainings = TrainingService.get_all_athlete(claims['userID'])
            elif claims['role'] == 'coach':
                trainings = TrainingService.get_all_coach(claims['userID'])
            else:
                return {"message": "no data found"}
        else:
            try:
                if claims['role'] == 'athlete':
                    trainings = TrainingService.get_by_args_athlete(claims['userID'], **TrainingSchema().load(dict(request.args.items())))
                elif claims['role'] == 'coach':
                    trainings = TrainingService.get_by_args_coach(claims['userID'], **TrainingSchema().load(dict(request.args.items())))
            except ValidationError as err:
                return err.messages
            except KeyError as err:
                return {"error": "wrong data provided"}
        return TrainingSchema().dump(trainings, many=True)


class Exercises(Resource):
    def get(self, id):
        result = ExercisesService.get_by_id(id)
        return ExerciseSchema().dump(result, many=True)
