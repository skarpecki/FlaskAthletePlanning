from flask import request, make_response, jsonify
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
            training = TrainingService.get_by_id(training_id, claims)
            status = 404 if training is None else 200
            return make_response(TrainingSchema().dump(training), status)
        except ValidationError as err:
            return make_response(err.messages, 400)



    @catch_jwt_exceptions
    @jwt_required
    def put(self, training_id):
        claims = get_jwt_claims()
        try:
            # feedback should be sent as {"feedback": "text"}
            args = request.get_json(force=True)
            return_json = {}
            if 'feedback' in args:
                feedback = TrainingService.add_feedback(training_id, claims, args['feedback'])
            if 'date' in args:
                date = TrainingService.modify_date(training_id, claims, args['date'])
            if date is None and feedback is None:
                response = {}
                status = 404
            else:
                response = {"Modified content can be found under": "127.0.0.1:5000/trainings/{}".format(training_id)}
                status = 201
            return make_response(jsonify(response), status)
        except ValidationError as err:
            return make_response(jsonify(err.messages), 400)
        except Exception as err:
            return make_response(jsonify({"Error": str(err)}), 500)


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
                return make_response(jsonify(err.messages), 400)
            except KeyError as err:
                return make_response(jsonify({"error": "wrong data provided"}),400)
        if len(trainings) != 0:
            return make_response(jsonify(TrainingSchema().dump(trainings, many=True)), 200)
        else:
            return make_response(jsonify({"Message": "No training found"}), 204)

    @catch_jwt_exceptions
    @jwt_required
    def post(self):
        claims = get_jwt_claims()
        try:
            attrs = TrainingSchema().load(request.get_json(force=True))
            training_id = TrainingService.create(claims, attrs)
            response = {"Created training can be found under":
                        "127.0.0.1:5000/trainings/{}".format(training_id)}
            return make_response(jsonify(response), 201)
        except ValidationError as err:
            return make_response(jsonify(err.messages), 400)


class Exercises(Resource):
    @catch_jwt_exceptions
    @jwt_required
    def get(self, training_id):
        claims = get_jwt_claims()
        try:
            exercises = ExercisesService.get_all(training_id, claims)
            status = 404 if exercises is None or len(exercises) == 0 else 200
            return make_response(jsonify(ExerciseSchema().dump(exercises, many=True)), status)
        except ValidationError as err:
            return make_response(jsonify(err.messages), 400)

    @catch_jwt_exceptions
    @jwt_required
    def post(self, training_id):
        claims = get_jwt_claims()
        try:
            attrs = ExerciseSchema().load(request.get_json(force=True))
            exercise = ExercisesService.create(training_id, claims, attrs)
            if exercise is None:
                response = {}
                status = 404
            else:
                response = {"Created exercise can be found under":
                            "127.0.0.1:5000/trainings/{}/exercises".format(training_id)}
                status = 201
            return make_response(jsonify(response), status)
        except ValidationError as err:
            return make_response(jsonify(err.messages), 400)
        except AttributeError as err:
            return {"Error": "No such training found"}

class ExercisesWithID(Resource):
    @catch_jwt_exceptions
    @jwt_required
    def get(self, training_id, exercise_id):
        claims = get_jwt_claims()
        try:
            exercise = ExercisesService.get_by_id(training_id, exercise_id, claims)
            status = 404 if exercise is None else 200
            return make_response(jsonify(ExerciseSchema().dump(exercise)), status)
        except ValidationError as err:
            return make_response(jsonify(err.messages), 400)

    @catch_jwt_exceptions
    @jwt_required
    def put(self, training_id, exercise_id):
        claims = get_jwt_claims()
        try:
            attrs = ExerciseUpdateSchema().load(request.get_json(force=True))
            exercise = ExercisesService.update(training_id, exercise_id, claims, **attrs)
            if exercise is None:
                response = {}
                status = 404
            else:
                response = {"Updated content can be find under":
                           "127.0.0.1:5000/trainings/{}/exercises/{}".format(training_id, exercise_id)}
                status = 201
            return make_response(jsonify(response), status)
        except ValidationError as err:
            return make_response(jsonify(err.messages), 400)


    @catch_jwt_exceptions
    @jwt_required
    def delete(self, training_id, exercise_id):
        claims = get_jwt_claims()
        try:
            exercise = ExercisesService.delete(training_id, exercise_id, claims)
            if exercise is None:
                response = {}
                status = 404
            else:
                response = {"message": "Successfully deleted exercise of id: {}".format(exercise_id)}
                status = 200
            return make_response(jsonify(response), status)
        except ValidationError as err:
            return make_response(jsonify(err.messages), 400)
