from app import db
from .model import Training
from .model import Exercise
from ..users.model import  User

class TrainingService():
    @staticmethod
    def get_all() -> list:
        result = Training.query.join(User).all()
        return result

class ExercisesService():
    @staticmethod
    def get_all() -> list:
        result = Exercise.query.join(Training).all()
        return result

    @staticmethod
    def get_by_args(**kwargs):
        result = Exercise.query.join(Training).filter_by(**kwargs).all()
        return result
