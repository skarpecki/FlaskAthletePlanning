from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from .service import TrainingService, ExercisesService
from .schema import TrainingSchema, ExerciseSchema
from .model import Training


class Trainings(Resource):
    def get(self) -> dict:
        if not request.args:
            Trainings = TrainingService.get_all();
            return TrainingSchema().dump(Trainings, many=True)


class Exercises(Resource):
    def get(self) -> dict:
        if not request.args:
            Exercises = ExercisesService.get_all()
        else:
            try:
                Exercises = ExercisesService.get_by_args(**request.args)
            except ValidationError as err:
                return err.messages

        return ExerciseSchema().dump(Exercises, many=True)
